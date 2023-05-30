from whoosh import writing
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from whoosh.analysis import StemmingAnalyzer
from whoosh.support.charset import accent_map
import os, tempfile

from .base_operator import BaseOperator


class FullTextSearch(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Full Text Search'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "output_budget_words",
                "data_type": "integer",
                "placeholder": "Enter maximum number of words in output"
            },
            {
                "name": "max_num_results",
                "data_type": "integer",
                "placeholder": "Enter maximum number of results"
            },
            {
                "name": "result_context_length",
                "data_type": "integer",
                "placeholder": "Enter context length around result in characters"
            },
            {
                "name": "query",
                "data_type": "string",
                "placeholder": "Enter your query"
            }
        ]
     
    @staticmethod   
    def declare_inputs():
        return [
            {
                "name": "text",
                "data_type": "string",
            },
            {
                "name": "query",
                "data_type": "string",
                "optional": "1"
            },
        ]
    
    @staticmethod 
    def declare_outputs():
        return [
            {
                "name": "search_results",
                "data_type": "string[]",
            },
            {
                "name": "search_results_metadata",
                "data_type": "{}[]",
            }
        ]

    def run_step(self, step, ai_context):
        p = step['parameters']
        text = ai_context.get_input('text', self)
        query = ai_context.get_input('query', self) or p['query']
        output_budget_words = p['output_budget_words']
        max_num_results = p['max_num_results']
        result_context_length = p['result_context_length']

        schema = Schema(content=TEXT(phrase=False, analyzer=StemmingAnalyzer()))

        storage = RamStorage()
        index = storage.create_index(schema)

        # Add the input text to the index
        writer = index.writer()
        writer.add_document(content=text)
        writer.commit()

        with index.searcher() as searcher:
            parser = QueryParser("content", index.schema)
            q = parser.parse(query)

            results = searcher.search(q, limit=max_num_results)
            result_strings = []
            result_metadata = []

            for hit in results:
                start_pos = max(0, hit.startchar - result_context_length)
                end_pos = min(len(text), hit.endchar + result_context_length)
                result = text[start_pos:end_pos]
                result_strings.append(result)
                result_metadata.append({
                    'position': hit.pos,
                    'start_char': hit.startchar,
                    'end_char': hit.endchar
                })

                if len(' '.join(result_strings).split()) > output_budget_words:
                    break

        ai_context.set_output('search_results', result_strings, self)
        ai_context.set_output('search_results_metadata', result_metadata, self)

        os.rmdir(index_dir)

