import json

from .base_operator import BaseOperator
from ai_context import AiContext

class ReadJsonValues(BaseOperator):
    @staticmethod
    def declare_name():
        return 'ReadJsonValues'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "keys",
                "data_type": "string",
                "placeholder": "Ex: 'key1,key2,key3'"
            }
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "json_string",
                "data_type": "string",
                "placeholder": "Enter the JSON string"
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "json_values",
                "data_type": "string",
            }
        ]

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        json_string = ai_context.get_input('json_string', self)
        params = step['parameters']
        keys = params.get('keys').split(',')

        try:
            json_object = json.loads(json_string)
            values = []

            for key in keys:
                values.append(f'{key}: {json_object.get(key)}')

            json_values = ', '.join(values)

            ai_context.add_to_log(f"Successfully read JSON values")
            ai_context.set_output('json_values', json_values, self)

        except Exception as e:
            ai_context.add_to_log(f"Failed to read JSON values. Error: {e}", color='red')
