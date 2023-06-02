import spacy
import heapq
import os, tempfile
from collections import deque

from .base_operator import BaseOperator

nlp = spacy.load("en_core_web_sm")

class FullTextSearch(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Full Text Search'
 
 
    @staticmethod
    def declare_description():
        return """Scan input text in sliding window fashion and return up to 'nresults' 
               windows that are most relevant to 'query' input/parameter. Setting 'multiline' to false
               would force results to be within single line."""
 
 
    @staticmethod
    def declare_allow_batch():
        return True
 
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.MANIPULATE_DATA.value

    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "nresults",
                "data_type": "integer",
                "placeholder": "Enter maximum number of search results. Default is 5."
            },
            {
                "name": "window_size",
                "data_type": "integer",
                "placeholder": "Search window size in words, default is 20"
            },
            {
                "name": "query",
                "data_type": "string",
                "placeholder": "Enter your query"
            }
            ,
            {
                "name": "multiline",
                "data_type": "boolean",
                "placeholder": "Whether to allow windows span multiple lines."
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
                "name": "search_result",
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
        nresults = int(p.get('nresults') or 5)
        window_size = int(p['window_size'] or 20)
        # TODO(misha): add boolean support on UI so that it would be dropdown and not this.
        multiline = p.get('multiline') in ['true', '1', 'True', 1]
        t = nlp(text)
        
        query_tokens = [token.text.lower() for token in nlp(query) if self.token_is_word(token)]
        
        # qd[i] stores a deque of all the entries of query_tokens[i] in t.
        # deque elements are tuples (position, match_score)
        qd = [deque() for _ in range(len(query_tokens))] 
        # Max score of each query token in current window
        s = [0] * len(query_tokens)
        total_s = 0
        # maps token index in 't' to index of token in query_tokens if it is matching it.
        token_id = {}

        # result is a heap of tuples (score, [window_start, window_end])
        results = []

        be_i = 0
        en_i = -1
        # [be_i, en_i] define the segment in the input text of tokens 't'.

        # When window end is last token in the text it should quit the sliding window loop.
        while en_i < len(t) - 1:
            # Moving en_i forward
            en_i += 1
            if not multiline and t[en_i].is_space and '\n' in str(t[en_i]):
                # We found end of line. Nuking existing window and start over on next line.
                be_i = en_i
                total_s = 0
                for ind in range(len(qd)):
                    qd[ind].clear()
                s = [0] * len(query_tokens)
                continue
                
            if self.token_is_word(t[en_i]):
                for i in range(len(query_tokens)):
                    score = self.token_match_score(query_tokens[i], t[en_i])
                    if score:
                        # new token with index en_i is matching query token with index (or id) of i
                        token_id[en_i] = i
                        #print (f'FOUND MATCH:en_i = {en_i}, score={score} i={i} query_tokens[i] = {query_tokens[i]}, t[en_i] = {t[en_i]} all deques = {qd}')
                        qd[i].append((en_i, score))
                        if score > s[i]:
                            total_s += (score - s[i])
                            s[i] = score
                            
                        # We assume here that t[en_i] can match only one query token.
                        break
                        
            if (en_i - be_i + 1) > window_size:
                # Window grew too large, need to move be_i (beginning of the window) forward
                tid = token_id.get(be_i)
                if tid:
                    #print(f'before popleft:tid = {tid} qd[tid] = {qd[tid]}')
                    
                    # we are losing token that was matching a token from query
                    qd[tid].popleft()
                    total_s -= s[tid]
                    s[tid] = 0
                    # now add back most relevant match for the token id that is present in the current window.
                    max_s = 0
                    for tup in qd[tid]:
                        cur_score = tup[1]
                        max_s = max(max_s, cur_score)
                    
                    s[tid] = max_s
                    total_s += max_s    
                be_i += 1
                    
            # current window is now represented by [be_i, en_i] range of tokens from original text 't'
            # and total_s is its relevance score     
            res_score = -total_s * (float(en_i - be_i + 1) / window_size) 
            # print(f"PUSH: {res_score}, text: {self.token_range_to_string((be_i, en_i), t)}")
            heapq.heappush(results, (
                    res_score, 
                    (be_i, en_i)
                )
            )   


        # List of windows to be used to form output, each is a tuple (begin_token_index, end_token_index)
        res_w = []
        res_size = 0
        for i in range(nresults):
            if len(results):
                heap_top = heapq.heappop(results)
                # print(f'score = {heap_top[0]}, text = {self.token_range_to_string(heap_top[1], t)}')
                new_w = heap_top[1]
                if res_size > 0:
                    prev_w = res_w[res_size - 1]
                    if prev_w[0] <= new_w[0] and prev_w[1] >= new_w[0]:
                        # If previous and new windows overlap -> merge them into single window in res_w array.
                        res_w[res_size - 1][1] = max(res_w[res_size - 1][1], new_w[1])
                        continue
                
                res_w.append(list(new_w))
                res_size += 1
                
        # print(f'res_w = {res_w}')
                
        final_output = "...\n".join([self.token_range_to_string(w, t) for w in res_w])        

        ai_context.add_to_log(f'Search result: {final_output}')
        ai_context.set_output('search_result', final_output, self)
        # TODO: either kill metadata output or set it.


    def token_range_to_string(self, window, text):
        # print(f'token_range_to_string, window = {window}, text={text}')
        return ' '.join([str(text[i]) for i in range(window[0], window[1] + 1)])


    def token_match_score(self, t1, t2):
        return 1.0 if str(t1).lower() == str(t2).lower() else 0


    def token_is_word(self, token):
        return not token.is_punct and not token.is_space and not token.is_stop



