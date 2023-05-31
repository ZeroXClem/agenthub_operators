import os
import io
import requests
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
        return []

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
        # Make sure Pandas data frames don't truncate cells of tables inside of PDF document.
        pd.set_option('display.max_colwidth', None)
        response = requests.get(params['pdf_uri'])
        pdf_content = io.BytesIO(response.content)
        df_list = tabula.read_pdf(pdf_content, pages='all')
        pdf_content = "\n".join(df.to_string(index=False) for df in df_list)
        #ai_context.add_to_log(f'PDF content: {pdf_content}')
        ai_context.set_output('pdf_content', pdf_content, self)
        
