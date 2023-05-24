import os
import requests
import tempfile

from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader

from .base_operator import BaseOperator

from ai_context import AiContext


class IngestPDF(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Ingest PDF'

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "pdf_uri", # testing: https://arxiv.org/pdf/2302.03803.pdf
                "data_type": "string",
                "placeholder": "Enter the URL of the PDF"
            }
        ]

    @staticmethod
    def declare_inputs():
        return []

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "pdf_content",
                "data_type": "Document[]",
            }
        ]

    def run_step(
            self,
            step,
            ai_context: AiContext,
    ):
        params = step['parameters']
        self.ingest(params, ai_context)

    def ingest(self, params, ai_context):
        pdf_uri = params.get('pdf_uri')
        ai_context.storage['ingested_pdf_url'] = pdf_uri
        if self.is_url(pdf_uri):
            text = self.load_pdf(pdf_uri)
            
            print(f'Inget PDF: text = {text}, type(text) = {type(text)}')
            
            ai_context.set_output('pdf_content', text, self)
            ai_context.add_to_log(f"Content from {pdf_uri} has been scraped.")
        else:
            pass  # leave unimplemented for ingesting files later

    def is_url(self, pdf_uri):
        # add url validation maybe?
        return True

    def load_pdf(self, url):
        with tempfile.TemporaryDirectory() as tmpdir:
            response = requests.get(url, stream=True)
            path = os.path.join(tmpdir, 'output.pdf')

            with open(path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            loader = DirectoryLoader(tmpdir, glob="**/*.pdf", loader_cls=PyMuPDFLoader)
            data = loader.load()

            # init empty string
            content = ""

            # merge page contents
            for doc in data:
                content += doc.page_content + "\n"

            return data

