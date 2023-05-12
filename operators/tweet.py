import json
import tweepy

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
        secret = "{" + ai_context.get_secret('twitter_api_key') + "}"
        twitter_secret = json.loads(secret)
        self.bearer_token = twitter_secret['BEARER_TOKEN']
        self.consumer_key = twitter_secret['CONSUMER_KEY']
        self.consumer_secret = twitter_secret['CONSUMER_SECRET']
        self.access_token = twitter_secret['ACCESS_TOKEN']
        self.access_token_secret = twitter_secret['ACCESS_SECRET']

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

    def send_tweet(self, tweet_text, url, ai_context):
        client = tweepy.Client(bearer_token=self.bearer_token)
        client = tweepy.Client(
            consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
            access_token=self.access_token, access_token_secret=self.access_token_secret
        )
        formatted_tweet_text = f"{tweet_text}\n{url}"
    
        try:
            response = client.create_tweet(
                text=formatted_tweet_text
            )
            ai_context.add_to_log(f"Tweet is live at: https://twitter.com/user/status/{response.data['id']}", color='green')
            
        except tweepy.TweepyException  as e:
            print(str(e))
            return f"Error sending tweet: {str(e)}"

