from .base_operator import BaseOperator
from ai_context import AiContext

class CombineStrings(BaseOperator):
    @staticmethod
    def declare_name():
        return 'CombineStrings'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "format",
                "data_type": "string",
                "placeholder": "Ex: 'This is input 1: {input1} This is input 2: {input2}'"
            }
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "input1",
                "data_type": "string",
                "placeholder": "Enter the first input string"
            },
            {
                "name": "input2",
                "data_type": "string",
                "placeholder": "Enter the second input string"
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "combined_string",
                "data_type": "string",
            }
        ]

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        input1 = ai_context.get_input('input1', self)
        input2 = ai_context.get_input('input2', self)
        params = step['parameters']
        format_string = params.get('format')
        try:
            combined_string = format_string.format(input1=input1, input2=input2)
            ai_context.add_to_log(f"Successfully combined strings")
            ai_context.set_output('combined_string', combined_string, self)

        except Exception as e:
            ai_context.add_to_log(f"Failed to combine strings. Error: {e}", color='red') 
