from .base_operator import BaseOperator

from ai_context import AiContext


class CastType(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Cast Type'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value
   
    @staticmethod     
    def declare_parameters():
        return [
            {
                "name": "output_type",
                "data_type": "string",
                "placeholder": "Output type to cast to."
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return [
            {
                "name": "input",
                "data_type": "any",
            }
        ]
    
    @staticmethod    
    def declare_outputs():
        return [
            {
                "name": "output",
                "data_type": "any",
            }
        ]

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        input = ai_context.get_input('input', self)  # >_<
        input_type = ai_context.get_input_type('input', self)
        output_type = step['parameters'].get('output_type')
        if input_type == "Document[]":
            if output_type == 'string':
                # Document schema from lanchain for reference: 
                # https://github.com/hwchase17/langchain/blob/master/langchain/schema.py#L269
                res = " ".join([d.page_content for d in input])
                ai_context.set_output('output', res, self)
                return True
            
       
        self.log_cannot_cast(input_type, output_type, ai_context)
        return False
            
            
    def log_cannot_cast(self, it, ot, ai_context):
        ai_context.add_to_log(
            f'\'{self.declare_name()}\' operator does not know how to convert {it} to {ot} ', 
            color='red'
        )
