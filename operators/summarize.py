from langchain import OpenAI, PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from .base_operator import BaseOperator

from ai_context import AiContext


class Summarize(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Summarize Content'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.AI.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "temperature",
                "data_type": "float",
                "placeholder": "Enter Temperature (Optional: Default is 0.2)"
            }
        ]

    @staticmethod
    def declare_inputs():
        return [     
            {
                "name": "rts_processed_content",
                "data_type": "string",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
             {
                "name": "summarize_gpt_response",
                "data_type": "string",
            }
        ]

    def run_step(
            self,
            step,
            ai_context: AiContext
    ):
        params = step['parameters']
        gpt_response = self.process(params=params, ai_context=ai_context)
        ai_context.set_output('summarize_gpt_response', gpt_response, self)
        ai_context.add_to_log(f"Response from GPT: {gpt_response}")

    def process(self, params, ai_context):
        response = self.chain(
            params=params,
            data=ai_context.get_input('rts_processed_content', self), 
            openai_api_key=ai_context.get_secret('openai_token')
        )
        return response

    def chain(self, params, data, openai_api_key):
        temperature = params.get('temperature', '0.2')
        # llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

        if temperature:
            temperature = float(temperature)
        else:
            temperature = 0.2

        llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=temperature)
        chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
        response = chain.run(data)
        return response


