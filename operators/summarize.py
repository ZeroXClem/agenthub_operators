from langchain import OpenAI, PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

from .base_operator import BaseOperator

from ai_context import AiContext


class Summarize(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Summarize Content'

    @staticmethod
    def declare_parameters():
        return [
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
        gpt_response = self.process(ai_context=ai_context)
        ai_context.set_output('summarize_gpt_response', gpt_response, self)
        ai_context.add_to_log(f"Response from GPT: {gpt_response}")

    def process(self, ai_context):
        response = self.chain(
            data=ai_context.get_input('rts_processed_content', self), 
            openai_api_key=ai_context.get_secret('openai_token')
        )
        return response

    def chain(self, data, openai_api_key):
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        prompt_template = """Write a concise summary of the following:\n\n{text}\n\nANSWER:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
        response = chain.run(data)
        return response

