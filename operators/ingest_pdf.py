import os
import io
import requests
import tempfile

from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from google.cloud import storage
import tabula
import pandas as pd

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
                "name": "pdf_uri",
                "data_type": "string",
                "placeholder": "Enter the URL of the PDF"
            }
            # TODO: uncomment when there are more than 1 methods of parsing PDF.
            #, 
            #{
            #    "name": "pdf_parsing_method",
            #    "data_type": "string",
            #    "placeholder": "default=tabula - for preservation of tables and spreadsheets"
            #}
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "file_name",
                "data_type": "string",
                "optional": "1"
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
            file_data = self.load_pdf_from_storage(file_name, ai_context)

        elif self.is_url(pdf_uri):
            file_data = self.load_pdf_from_uri(pdf_uri)
        
        text = self.read_pdf(file_data)
        ai_context.set_output('pdf_content', text, self)
        ai_context.add_to_log(f"Content from {file_name} has been scraped.")
        ai_context.add_to_log(f"Scraped data {text}")

    def is_url(self, pdf_uri):
        # add url validation maybe?
        return True

    def load_pdf_from_uri(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response
        return response.content

    # def download_file(self, file_name, ai_context):
    #     # Use the tempfile module to create a temporary directory
    #     temp_dir = tempfile.mkdtemp()

    #     # Create the full path to the temporary file
    #     local_file_path = os.path.join(temp_dir, file_name)

    #     # Get the file data from ai_context
    #     file_data = ai_context.get_file(file_name, ai_context.get_run_id())

    #     # Write the file data to the temporary file
    #     with open(local_file_path, 'wb') as temp_file:
    #         temp_file.write(file_data)
        
    #     # Return the path to the temporary file
    #     return local_file_path
    
    def load_pdf_from_storage(self, file_name, ai_context):
        file_data = ai_context.get_file(file_name, ai_context.get_run_id())
        return file_data
    
    def read_pdf(self, pdf):
        pd.set_option('display.max_colwidth', None)
        pdf_content = io.BytesIO(pdf)
        df_list = tabula.read_pdf(pdf_content, pages='all')
        pdf_content = "\n".join(df.to_string(index=False) for df in df_list)
        
        return pdf_content
    
        # Make sure Pandas data frames don't truncate cells of tables inside of PDF document.
        # pd.set_option('display.max_colwidth', None)
        # response = requests.get(params['pdf_uri'])
        # pdf_content = io.BytesIO(response.content)
        # df_list = tabula.read_pdf(pdf_content, pages='all')
        # pdf_content = "\n".join(df.to_string(index=False) for df in df_list)
        # #ai_context.add_to_log(f'PDF content: {pdf_content}')
        # ai_context.set_output('pdf_content', pdf_content, self)
        
