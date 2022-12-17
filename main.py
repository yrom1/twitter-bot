from os import environ
from typing import *  # type: ignore

import tweepy


class Twitter:
    def __init__(self):
        self.api = self.get_twitter_api()

    def get_twitter_api(self) -> tweepy.API:
        consumer_key = environ["TWITTER_BOT_API_KEY"]
        consumer_secret = environ["TWITTER_BOT_API_KEY_SECRET"]
        access_token = environ["TWITTER_BOT_ACCESS_TOKEN"]
        access_token_secret = environ["TWITTER_BOT_ACCESS_TOKEN_SECRET"]
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        return tweepy.API(auth)

    def make_tweet(self, tweet: str) -> None:
        self.api.update_status(tweet)

    def print_user_tweet(self, user: str) -> None:
        ans: List[str] = []
        for status in tweepy.Cursor(self.api.user_timeline, screen_name=user, tweet_mode="extended").items():
            print(status.full_text)
            break

if __name__ == '__main__':
    Twitter().print_user_tweet("geoffreyhinton")
    Twitter().make_tweet('Hello, world!')
