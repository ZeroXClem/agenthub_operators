import requests
import re

from bs4 import BeautifulSoup

from ai_context import AiContext

from .base_operator import BaseOperator


class IngestData(BaseOperator):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def declare_name():
        return 'Ingest Data'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "data_uri",
                "data_type": "string",
                "placeholder": "Enter the URL to browse"
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return [
            {
                "name": "input_url",
                "data_type": "string",
            }
        ]
    
    @staticmethod    
    def declare_outputs():
        return [
            {
                "name": "uri_content",
                "data_type": "string",
            }
        ]

    def run_step(
        self, 
        step, 
        ai_context: AiContext
    ):
        params = step['parameters']
        self.ingest(params, ai_context)

    def ingest(self, params, ai_context):
        data_uri = params.get('data_uri', None)
        if not data_uri:
            data_uri = ai_context.get_input('input_url', self)
        ai_context.storage['ingested_url'] = data_uri
        if self.is_url(data_uri):
            text = self.scrape_text(data_uri)
            ai_context.set_output('uri_content', text, self)
            ai_context.add_to_log(f"Content from {data_uri} has been scraped.")
        else:
            pass  # Leave unimplemented for ingesting files later

    def is_url(self, data_uri):
        # url_pattern = re.compile(
        #     r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        # return re.match(url_pattern, data_uri) is not None
        #HACKY WORKAROUND FOR NOW, WAS BREAKING DURING DEMO
        return True

    def scrape_text(self, url):
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "html.parser")

        for script in bs(["script", "style"]):
            script.extract()

        text = bs.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)

        return text

