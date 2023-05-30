from .base_operator import BaseOperator

from ai_context import AiContext


class ListProcessor(BaseOperator):
    @staticmethod
    def declare_name():
        return 'List Processor'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.AI.value
   
    @staticmethod     
    def declare_parameters():
        return [
            {
                "name": "prompt",
                "data_type": "string",
                "placeholder": "What should the AI do with this list?"
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return [
            {
                "name": "list",
                "data_type": "{name,content}[]",
            }
        ]
    
    @staticmethod    
    def declare_outputs():
        return [
            {
                "name": "result_list",
                "data_type": "{name,content}[]",
            }
        ]

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        l = ai_context.get_input('list', self)
        if l is None:
            ai_context.add_to_log(
                "ListProcessor is expecting 'list' entry in AiContext, it should be set there "
                "by one of the operators in the pipeline that run prior to ListProcessor", color='red')
            return False

        result_list = []
        for e in l:
            content = e['content']
            prompt = f'''Given the content:
{content}
Address the goal:
{step['parameters']['prompt']}
            '''
            msgs = [prompt]
            ai_response = ai_context.run_chat_completion(prompt=prompt)
            
            element_title_str = f"ListProcessor: element name: {e.get('name')}"
            ai_context.add_to_log(element_title_str, color='green')
            ai_context.add_to_log(f"Response from AI:\n{ai_response}", save=True)
            
            result_list.append({
                'name': e['name'],
                'content': ai_response
            })
            
        ai_context.set_output('result_list', result_list, self)
        return True

        
