import os
import requests
import tempfile

from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from google.cloud import storage

from .base_operator import BaseOperator

from ai_context import AiContext


class IngestPDF(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Ingest PDF'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.CONSUME_DATA.value

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
        return [
            {
                "name": "file_name",
                "data_type": "string",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "pdf_content",
                "data_type": "string",
            }
        ]

    def run_step(
            self,
            step,
            ai_context: AiContext,
    ):
        params = step['parameters']
        pdf_uri = params.get('pdf_uri')
        file_name = ai_context.get_input('file_name', self)
        self.ingest(pdf_uri, file_name, ai_context)

    def ingest(self, pdf_uri, file_name, ai_context):
        # If file name has been provided via input, it takes precedence over pdf_uri
        if file_name:
            local_file_path = self.download_file(file_name, ai_context)
            text = self.load_pdf_from_local_file(local_file_path)

        elif self.is_url(pdf_uri):
            ai_context.storage['ingested_pdf_url'] = pdf_uri
            text = self.load_pdf_from_uri(pdf_uri)
            
        ai_context.set_output('pdf_content', text, self)
        ai_context.add_to_log(f"Content from {file_name} has been scraped.")
        ai_context.add_to_log(f"Scraped data {text}")

    def is_url(self, pdf_uri):
        # add url validation maybe?
        return True

    def load_pdf_from_uri(self, url):
        with tempfile.TemporaryDirectory() as tmpdir:
            response = requests.get(url, stream=True)
            path = os.path.join(tmpdir, 'output.pdf')
            with open(path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return self.load_pdf_from_local_file(path)

    def load_pdf_from_local_file(self, path):
        loader = DirectoryLoader(os.path.dirname(path), glob="**/*.pdf", loader_cls=PyMuPDFLoader)
        data = loader.load()

        # init empty string
        content = ""

        # merge page contents
        for doc in data:
            content += doc.page_content + "\n"
        return content  # Returning content (string) instead of data (Document)

    def download_file(self, file_name, ai_context):
        # Use the tempfile module to create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Create the full path to the temporary file
        local_file_path = os.path.join(temp_dir, file_name)

        # Get the file data from ai_context
        file_data = ai_context.get_file(file_name, ai_context.get_run_id())

        # Write the file data to the temporary file
        with open(local_file_path, 'wb') as temp_file:
            temp_file.write(file_data)
        
        # Return the path to the temporary file
        return local_file_path
