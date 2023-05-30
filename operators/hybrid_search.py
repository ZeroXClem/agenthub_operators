from ai_context import AiContext

from .base_operator import BaseOperator
from .util import (
    sort_chunks_by_similarity,
    select_most_relevant_chunks,
    get_max_tokens_for_model,
    count_tokens
)


class HybridSearch(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Hybrid Search'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.AI.value
    
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
        query_emb = ai_context.embed_text(query)
        
        sorted_chunks = sort_chunks_by_similarity(
            query_emb, 
            ai_context.get_input('vector_index', self)
        )
        prompt = f"Given the following context, and any prior knowledge you have, {query}?"
        num_tokens_spent = count_tokens(prompt, ai_context.get_model_name())
        token_limit = get_max_tokens_for_model(ai_context.get_model_name())
        # We reserve 250 tokens for the response.
        token_budget = token_limit - 250 - num_tokens_spent
        
        selected_chunks = select_most_relevant_chunks(
            sorted_chunks, 
            token_budget, 
            ai_context.get_model_name()
        )
        ai_context.add_to_log("{} embeddings were fit into the prompt".format(len(selected_chunks)))
        
        selected_chunks_str = str(selected_chunks)
        prompt += f" context: {selected_chunks_str}"  
              
        ai_response = ai_context.run_chat_completion(prompt=prompt)
        ai_context.set_output('hybrid_search_chatgpt_response', ai_response, self)
        ai_context.add_to_log(f'Response from ChatGPT + Hybrid Search: {ai_response}')


