import requests
from bs4 import BeautifulSoup
import json

from .base_operator import BaseOperator
from ai_context import AiContext

class ScrapeHackerNews(BaseOperator):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def declare_name():
        return 'Scrape Hacker News'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "keywords",
                "data_type": "json",
                "placeholder": "Enter keywords to filter news (optional)"
            },
            {
                "name": "num_pages",
                "data_type": "integer",
                "placeholder": "Enter the number of pages to scrape (max 5 pages)"
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return []
    
    @staticmethod    
    def declare_outputs():
        return [
            {
                "name": "title_link_dict",
                "data_type": "json",
            }
        ]

    def run_step(
        self, 
        step, 
        ai_context: AiContext, 
    ):
        params = step['parameters']
        self.scrape_hacker_news(params, ai_context)

    def scrape_hacker_news(self, params, ai_context):
        keywords = params.get('keywords', [])
        num_pages = int(params.get('num_pages', 1))  # Convert to int here
        excluded_words = ['AskHN', 'ShowHN', 'LaunchHN']

        if num_pages > 5:
            ai_context.add_to_log(f"Maximum limit of 5 pages exceeded. Please provide a number up to 5.")
            return

        title_link_dict = {}

        for page_num in range(1, num_pages + 1):
            response = requests.get(f'https://news.ycombinator.com/?p={page_num}')
            bs = BeautifulSoup(response.text, "html.parser")
            posts = bs.select('tr.athing')  # select each post

            for post in posts:
                title_element = post.select_one('.titleline > a')  # select the title element within the post
                if title_element:
                    title = title_element.text
                    link = title_element['href']

                    # Check if any keyword is in the title (if keywords are provided)
                    if keywords and not any(keyword.lower() in title.lower() for keyword in keywords):
                        continue

                    # Check if none of the excluded words are in the title
                    if any(excluded_word in title for excluded_word in excluded_words):
                        continue

                    title_link_dict[title] = link

        ai_context.set_output('title_link_dict', json.dumps(title_link_dict), self)
        ai_context.add_to_log(f"{num_pages} page(s) of Hacker News have been scraped and filtered.")

        ai_context.set_output('title_link_dict', json.dumps(title_link_dict), self)
        ai_context.add_to_log(f"{num_pages} page(s) of Hacker News have been scraped and filtered.")
