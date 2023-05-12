from langchain.text_splitter import RecursiveCharacterTextSplitter

from .base_operator import BaseOperator

from ai_context import AiContext


class SplitData(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Recursively Split Text'

    @staticmethod
    def declare_parameters():
        return [
            # {
            #     "name": "chunk_size",
            #     "data_type": "integer",
            #     "placeholder": "Enter Chunk Size (Optional: Default is 2000)"
            # },
            # {
            #     "name": "chunk_overlap",
            #     "data_type": "integer",
            #     "placeholder": "Enter Chunk Overlap (Optional: Default is 100)"
            # }
        ]

    @staticmethod
    def declare_inputs():
        return [     
            {
                "name": "text",
                "data_type": "string",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "rts_processed_content",
                "data_type": "string",
            }
        ]

    def run_step(
            self,
            step,
            ai_context: AiContext
    ):
        text = ai_context.get_input('text', self)
        split_text = self.process(text, ai_context)
        ai_context.set_output('rts_processed_content', split_text, self)
        ai_context.add_to_log("Successfully split text!")

    def process(self, text, ai_context):
        content = text
        formatted = self.split(content)
        return formatted

    def split(self, content):
        chunk_size: str = 2000
        chunk_overlap: str = 100
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(content)
        return texts

