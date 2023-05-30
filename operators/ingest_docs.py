import os
import tempfile
import asyncio
import aiohttp


from langchain.document_loaders import ReadTheDocsLoader
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base_operator import BaseOperator
from ai_context import AiContext


class IngestDocs(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Ingest Documentation'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.CONSUME_DATA.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "docs_uri", # testing: https://python.langchain.com/en/latest/
                "data_type": "string",
                "placeholder": "Enter the URL of the Documentation"
            }
        ]

    @staticmethod
    def declare_inputs():
        return []

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "docs_content",
                "data_type": "string",
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
        docs_uri = params.get('docs_uri')
        ai_context.storage['ingested_docs_url'] = docs_uri
        if self.is_url(docs_uri):
            # text = self.load_docs(docs_uri)
            text = asyncio.run(self.load_docs(docs_uri))
            ai_context.set_output('docs_content', text, self)
            ai_context.add_to_log(f"Content from {docs_uri} has been scraped.")
        else:
            pass  # leave unimplemented for ingesting files later

    def is_url(self, docs_uri):
        # add url validation maybe?
        return True
    

    async def download_file(self, session, url, output_directory):
        async with session.get(url) as response:
            if response.status == 200:
                file_name = os.path.join(output_directory, os.path.basename(url))
                file_content = await response.read()
                with open(file_name, 'wb') as file:
                    file.write(file_content)
                print(f"Downloaded: {url}")
            else:
                print(f"Failed to scrape: {url}")

    async def load_docs(self, url):
        scraped_count = 0
        with tempfile.TemporaryDirectory() as temp_dir:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        tasks = []

                        for link in soup.find_all("a", href=True):
                            file_url = urljoin(url, link['href'])
                            if file_url.endswith('.html'):
                                tasks.append(self.download_file(session, file_url, temp_dir))

                        await asyncio.gather(*tasks)
                    else:
                        print("Failed to retrieve the page.")
            loader = ReadTheDocsLoader(temp_dir, features='html.parser', encoding='utf-8')
            data = loader.load()
            content = ""
            for doc in data:
                content += doc.page_content + "\n"

            return data

