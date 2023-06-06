from .base_operator import BaseOperator
from ai_context import AiContext
from urllib.parse import quote_plus

class EncodeURL(BaseOperator):
    @staticmethod
    def declare_name():
        return 'EncodeURL'

    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value

    @staticmethod
    def declare_parameters():
        return []

    @staticmethod
    def declare_allow_batch():
        return True

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "input",
                "data_type": "string",
                "placeholder": "Enter the input string to encode"
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "encoded_url",
                "data_type": "string",
            }
        ]

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        input_string = ai_context.get_input('input', self)
        try:
            encoded_url = quote_plus(input_string)
            ai_context.add_to_log(f"Successfully encoded URL")
            ai_context.set_output('encoded_url', encoded_url, self)

        except Exception as e:
            ai_context.add_to_log(f"Failed to encode URL. Error: {e}", color='red') 