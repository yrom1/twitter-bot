from os import environ

import tweepy

consumer_key = environ["TWITTER_BOT_API_KEY"]
consumer_secret = environ["TWITTER_BOT_API_KEY_SECRET"]
access_token = environ["TWITTER_BOT_ACCESS_TOKEN"]
access_token_secret = environ["TWITTER_BOT_ACCESS_TOKEN_SECRET"]

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)

# Create a tweepy API client
api = tweepy.API(auth)

# Post a tweet
api.update_status('Hello, world!')
