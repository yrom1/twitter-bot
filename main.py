from os import environ

import tweepy

consumer_key = environ["TWITTER_BOT_API_KEY"]
consumer_secret = environ["TWITTER_BOT_API_KEY_SECRET"]
access_token = environ["TWITTER_BOT_ACCESS_TOKEN"]
access_token_secret = environ["TWITTER_BOT_ACCESS_TOKEN_SECRET"]


auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)
# api.update_status('Hello, world!') # need ELEVATED PRIVILEGES

user = "geoffreyhinton"
for status in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items():
    print(status.full_text)
    break
