import json
import tweepy
import re

from .base_operator import BaseOperator

from ai_context import AiContext


class Tweet(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Tweet'

    @staticmethod
    def declare_parameters():
        return []

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "tweet_text",
                "data_type": "string",
                "placeholder": "Enter the text to tweet"
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "tweet_status",
                "data_type": "string",
            }
        ]
        
    def set_twitter_keys_and_secrets(self, ai_context):
        app_secrets = json.loads(ai_context.get_secret('twitter_app_auth'))
        user_secrets = json.loads(ai_context.get_secret('twitter_api_key'))        
        self.bearer_token = app_secrets['BEARER_TOKEN']
        self.consumer_key = app_secrets['CONSUMER_KEY']
        self.consumer_secret = app_secrets['CONSUMER_SECRET']
        self.access_token = user_secrets['ACCESS_TOKEN']
        self.access_token_secret = user_secrets['ACCESS_SECRET']

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        tweet_text = ai_context.get_input('tweet_text', self)
        url = ai_context.storage['ingested_url']
        self.set_twitter_keys_and_secrets(ai_context)

        tweet_status = self.send_tweet(tweet_text, url, ai_context)
        ai_context.set_output('tweet_status', tweet_status, self)
        ai_context.memory_add_to_list('tweeted_links', url)
         
    def trim_trailing_hashtags(self, text, url):
        words = text.split()
        while len(' '.join(words)) + len(url) > 280:
            if words[-1].startswith('#'):
                words = words[:-1]
            else:
                break
        return ' '.join(words)


    def send_tweet(self, tweet_text, url, ai_context):
        client = tweepy.Client(bearer_token=self.bearer_token)
        client = tweepy.Client(
            consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
            access_token=self.access_token, access_token_secret=self.access_token_secret
        )
                
        # If tweet is too long, remove trailing hashtags
        tweet_text = self.trim_trailing_hashtags(tweet_text, url)
            
        formatted_tweet_text = f"{tweet_text}\n{url}"

        ai_context.add_to_log(f'Tweeting: {formatted_tweet_text}')
        try:
            response = client.create_tweet(
                text=formatted_tweet_text
            )
            output = f"Tweet is live at: https://twitter.com/user/status/{response.data['id']}"
            ai_context.add_to_log(output, color='green')
            
        except tweepy.TweepyException  as e:
            print(str(e))
            output = f"Error sending tweet: {str(e)}"
            ai_context.add_to_log(output, color='red')
            
        return output

