import json

from .base_operator import BaseOperator


class InputOperator(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Input'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MISC.value
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "value",
                "data_type": "string",
                "placeholder": "Anything you would like this operator instance to output"
            }
        ]
     
    @staticmethod   
    def declare_inputs():
        return []
    
    @staticmethod 
    def declare_outputs():
        return [
            {
                "name": "output",
                "data_type": "string",
            }
        ]

    def run_step(self, step, ai_context):
        p = step['parameters']
        ai_context.set_output('output', p['value'], self)

        
        
