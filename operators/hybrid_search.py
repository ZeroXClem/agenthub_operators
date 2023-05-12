import argparse
import tiktoken
import numpy as np


from ai_context import AiContext

from .base_operator import BaseOperator

import openai
import logging
import heapq

from .util import get_max_tokens_for_model


def set_key(openai_token):
    openai.api_key = openai_token


class HybridSearch(BaseOperator):
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def declare_name():
        return 'Hybrid Search'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "query",
                "data_type": "string",
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return [
            {
                "name": "vector_index",
                "data_type": "{}",
            }
        ]
    
    @staticmethod    
    def declare_outputs():
        return [
             {
                "name": "hybrid_search_chatgpt_response",
                "data_type": "string",
            }
        ]

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        params = step['parameters']
        query = params.get('query')
        set_key(ai_context.get_secret('openai_token'))
        query_embedding = self.get_embedding(query)
        
        # Generate a heap of the most similar embeddings, we're unsure how many we can fit into the prompt at this point. 
        sorted_embeddings = self.calculate_sorted_similarities(query_embedding, ai_context.get_input('vector_index', self))
        # Format the message and determine how many tokens our contextless prompt is
        message = f"Given the following context, and any prior knowledge you have, {query}?"
        message_tokens = self.num_tokens_from_string(message)
        # Fit as many embeddings as we can into the prompt
        closest_embeddings = self.get_max_embeddings_fit(
            sorted_similarities=sorted_embeddings, 
            initial_tokens=message_tokens, 
            ai_context=ai_context
        )
        
        # Add context to message
        closest_embeddings_str = str(closest_embeddings)
        message += f" context: {closest_embeddings_str}"  
              
        msgs = [{"role": "user", "content": message}]
        ai_response = ai_context.run_chat_completion(msgs=msgs)
        ai_context.set_output('hybrid_search_chatgpt_response', ai_response, self)
        ai_context.add_to_log(f'Response from ChatGPT + Hybrid Search: {ai_response}')

    def get_embedding(self, text_or_tokens):
        EMBEDDING_MODEL = 'text-embedding-ada-002'
        return openai.Embedding.create(input=text_or_tokens, model=EMBEDDING_MODEL)["data"][0]["embedding"]

    def cosine_distance(self, emb1, emb2):
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    def calculate_sorted_similarities(self, query_embedding, embeddings_dict):
        sorted_similarities = []

        for embedding_key, text in embeddings_dict.items():
            embedding = np.array(embedding_key)  # Convert tuple to numpy array
            similarity = self.cosine_distance(query_embedding, embedding)
            heapq.heappush(sorted_similarities, (-similarity, embedding_key, text))

        return sorted_similarities

    def num_tokens_from_string(self, string: str, model_name: str = 'gpt-3.5-turbo') -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def get_max_embeddings_fit(self, sorted_similarities, initial_tokens, ai_context, model='gpt-3.5-turbo'):
        # Since OpenAI is applying a limit to combined tokens in the input prompt and the response
        # we want to make sure we leave enough space for the output by not overinflating the input prompt.
        MIN_RESPONSE_SIZE = 250
    
        selected_embeddings = []
        total_tokens = initial_tokens + MIN_RESPONSE_SIZE
        token_limit = get_max_tokens_for_model(model)
        
        for similarity, embedding_key, text in sorted_similarities:
            text_tokens = self.num_tokens_from_string(text, model)
            
            if total_tokens + text_tokens  < token_limit:
                total_tokens += text_tokens 
                selected_embeddings.append(text)
            else:
                break
        
        ai_context.add_to_log("{} embeddings were fit into the prompt".format(len(selected_embeddings)))
        return selected_embeddings

