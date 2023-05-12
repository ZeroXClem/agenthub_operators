import json

from .base_operator import BaseOperator


class AskChatGpt(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Ask ChatGPT'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "question",
                "data_type": "string",
                "placeholder": "Enter your question"
            },
            {
                "name": "context",
                "data_type": "string",
                "placeholder": "Enter context (optional)"
            },
            {
                "name": "max_tokens",
                "data_type": "integer",
                "placeholder": "Enter max tokens for response"
            }
        ]
     
    @staticmethod   
    def declare_inputs():
        return []
    
    @staticmethod 
    def declare_outputs():
        return [
            {
                "name": "chatgpt_response",
                "data_type": "string",
            }
        ]

    def run_step(self, step, ai_context):
        msgs = self.gen_prompt_messages(step, ai_context)
        ai_response = ai_context.run_chat_completion(msgs=msgs)
 
        ai_context.set_output('chatgpt_response', ai_response, self)
 
        ai_context.add_to_log(f'Response from ChatGPT: {ai_response}', save=True)
        
 
    def gen_prompt_messages(self, step, ai_context):
        ai_context.add_user_query(json.dumps(step['parameters']))
        return ai_context.messages
        
