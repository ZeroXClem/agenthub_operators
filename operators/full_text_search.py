import spacy
import heapq
import os, tempfile

from .base_operator import BaseOperator

nlp = spacy.load("en_core_web_sm")

class FullTextSearch(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Full Text Search'
 
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value

    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "max_num_results",
                "data_type": "integer",
                "placeholder": "Enter maximum number of results"
            },
            {
                "name": "window_size",
                "data_type": "integer",
                "placeholder": "Search window size in tokens, default is 100"
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
                "data_type": "string",
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
        max_num_results = int(p['max_num_results'] or 10)
        window_size = int(p['window_size'] or 100)
        doc = nlp(text)   
        
        query_tokens = [token.text.lower() for token in nlp(query) if self.token_is_word(token)]
        print(f'query_tokens = {query_tokens}')
        results = []

        for i in range(len(doc) - window_size + 1):
            window_tokens = [token.text.lower() for token in doc[i : i + window_size]]
            score = self.calculate_relevance(window_tokens, query_tokens)
            heapq.heappush(results, (-score, doc[i : i + window_size].text))

        output = []
        for i in range(max_num_results):
            if len(results):
                t = heapq.heappop(results)
                print(f'score = {t[0]}')
                output.append(t[1])

        # Join all strings in output list into a single string separated by newline
        output_string = "\n".join(output)
        ai_context.add_to_log(f'Search results: {output_string}')
        ai_context.set_output('search_results', output_string, self)


    def token_is_word(self, token):
        return not token.is_punct and not token.is_space and not token.is_stop


    def calculate_relevance(self, window_tokens, query_tokens):
        score = sum([window_tokens.count(token) for token in query_tokens ])
        return score

