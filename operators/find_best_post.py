from .base_operator import BaseOperator
from ai_context import AiContext
import json

class FindBestPost(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Find Best Post'

    @staticmethod
    def declare_parameters():
        return [
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
                "name": "title_link_dict",
                "data_type": "json",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "best_post_link",
                "data_type": "string",
            }
        ]

    def run_step(self, step, ai_context: AiContext):
        params = step['parameters']
        self.find_best_post(params, ai_context)

    def find_best_post(self, params, ai_context):
        query = params.get('query', '')
        posts = ai_context.get_input('title_link_dict', self)
        print("posts: ", posts)
        title_link_dict = json.loads(posts)
        
        
        
        used_links = ai_context.memory_get_list('tweeted_links')
        
        print(f"used_links = {used_links}\ntitle_link_dict = {title_link_dict}")
        title_link_dict = {title: url for title, url in title_link_dict.items() if url not in used_links}
        
        print(title_link_dict)
        # Converting titles into a context string
        context_string = ', '.join(title_link_dict.keys())
        
        ai_context.add_to_log(f"Analyzing {len(title_link_dict)} potential post(s).", self)

        # Final prompt string
        message = f"From the following post titles: {context_string}, pick the post that most closely reflects this desire: {query}? Return the title of the post selected and nothing else."

        # Here you can pass the prompt to your function
        msgs = [{"role": "user", "content": message}]
        best_post_title = ai_context.run_chat_completion(msgs=msgs)
        
        # Check if the title exists in the dictionary
        if best_post_title not in title_link_dict and best_post_title.endswith('.'):
            best_post_title = best_post_title[:-1]  # Remove the last character (the period)

        best_post_link = title_link_dict.get(best_post_title, '')

        ai_context.add_to_log(f"The most relevant post to your query is titled: {best_post_title}. With Link: {best_post_link}", self)
        
        ai_context.set_output('best_post_link', best_post_link, self)

