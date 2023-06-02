from .base_operator import BaseOperator

from ai_context import AiContext


class VectorizeOperator(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Vectorize'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value

    @staticmethod
    def declare_description():
        return """Creates a list out of 'element' of size len('vector') like so: [element] * len(vector)"""

    @staticmethod
    def declare_parameters():
        return [
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "element",
                "data_type": "any",
            },
            {
                "name": "vector",
                "data_type": "any",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "vector_of_elements",
                "data_type": "any",
            }
        ]

    def run_step(
            self,
            step,
            ai_context: AiContext,
    ):
        element = ai_context.get_input('element', self)
        dim = len(ai_context.get_input('vector', self))
        ai_context.set_output('vector_of_elements', [element] * dim, self)

        
