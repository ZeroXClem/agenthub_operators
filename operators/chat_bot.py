from ai_context import AiContext

from .base_operator import BaseOperator
from .util import (
    sort_chunks_by_similarity,
    select_most_relevant_chunks,
    get_max_tokens_for_model,
    count_tokens
)


class ChatBot(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Ask Chat Bot'
        
    @staticmethod
    def declare_description():
        return "Given a 'query' (parameter) it would use Vector Index ('vector_index_id' parameter) and conversation history of current user to answer the question stated in 'query'"

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "vector_index_id",
                "data_type": "string",
                "placeholder": "Vector Index Id, usually printed by Persist Vector Index"
            },
            {
                "name": "query",
                "data_type": "string",
                "placeholder": "Your question to Chat Bot."
            }
        ]

    @staticmethod
    def declare_inputs():
        return [
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "response",
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
        model_name = ai_context.get_model_name()
        vi_uuid = params['vector_index_id']
        
        print(f'vi_uuid = {vi_uuid}')
        
        vi = ai_context.get_vector_index(vi_uuid)

        token_limit = get_max_tokens_for_model(model_name)
        prompt = f"Given context below, answer: {query}?"
        num_tokens_spent = count_tokens(prompt, model_name)
        # We reserve 500 tokens for the response.
        context_token_budget = token_limit - 500 - num_tokens_spent
        hybrid_search_token_budget = int(0.6 * context_token_budget)
        chat_history_token_budget = context_token_budget - hybrid_search_token_budget

        # (1) Incorporate results of Hybrid search into prompt
        sorted_chunks = sort_chunks_by_similarity(
            query_emb, 
            vi
        )

        selected_chunks = select_most_relevant_chunks(
            sorted_chunks, 
            hybrid_search_token_budget, 
            model_name
        )
        
        ai_context.add_to_log("{} embeddings were fit into the prompt".format(len(selected_chunks)))
        
        selected_chunks_str = str(selected_chunks)
        prompt += f" Context: {selected_chunks_str}"
        
        # (2) Load chat history up to chat_history_token_budget
        # Note that right now chat history is bound to vector index id. So make sure to 
        # not change vector index id when rebuilding it.
        chat_history_memory_name = f'cb:{vi_uuid}'
        chat_history = ai_context.memory_get_list(chat_history_memory_name)
        history_tokens = 0
        first_history_msg = len(chat_history)
        for i in range(len(chat_history) - 1, -1, -1):
            token_count = count_tokens(chat_history[i]['content'], model_name)
            if (history_tokens + token_count) < chat_history_token_budget:
                history_tokens += token_count
                first_history_msg = i
            else:
                break
        
        msgs = chat_history[first_history_msg : ]
        msgs.append({"role": "user", "content": prompt})
        
        ai_response = ai_context.run_chat_completion(msgs=msgs)
        ai_context.set_output('response', ai_response, self)
        ai_context.add_to_log(f'Chat Bot response: {ai_response}', color='blue')
        ai_context.memory_add_to_list(chat_history_memory_name,
            [
                {"role": "user", "content": query},
                {"role": "system", "content": ai_response}
            ]
        )
    

