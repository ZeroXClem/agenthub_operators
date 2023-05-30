import json

from .base_operator import BaseOperator


class AskChatGpt(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Ask ChatGPT'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.AI.value
    
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
        return [
            {
                "name": "context",
                "data_type": "string",
                "optional": "1"
            },
        ]
    
    @staticmethod 
    def declare_outputs():
        return [
            {
                "name": "chatgpt_response",
                "data_type": "string",
            }
        ]

    def run_step(self, step, ai_context):
        p = step['parameters']
        input_context = ai_context.get_input('context', self)
        prompt = p['question']
        param_context = p.get('context')
        
        if input_context and param_context:
            context = f'[{input_context}] [{param_context}]'
        elif input_context:
            context = f'[{input_context}]'
        elif param_context:
            context = f'[{param_context}]'
        else:
            context = None

        if context:
            prompt = f'Given the context: {context}, answer the question or complete the following task: {prompt}'

        ai_response = ai_context.run_chat_completion(prompt=prompt)
        ai_context.set_output('chatgpt_response', ai_response, self)
        ai_context.add_to_log(f'Response from ChatGPT: {ai_response}', save=True)

        
        
