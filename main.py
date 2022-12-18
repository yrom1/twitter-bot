from __future__ import annotations

from os import environ
from typing import *  # type: ignore

import tweepy
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection


class Twitter:
    def __init__(self):
        self.api = self.get_twitter_api()

    def get_twitter_api(self) -> tweepy.API:
        consumer_key = environ["TWITTER_BOT_API_KEY"]
        consumer_secret = environ["TWITTER_BOT_API_KEY_SECRET"]
        access_token = environ["TWITTER_BOT_ACCESS_TOKEN"]
        access_token_secret = environ["TWITTER_BOT_ACCESS_TOKEN_SECRET"]
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def make_tweet(self, tweet: str) -> None:
        self.api.update_status(tweet)

    def get_tweet(self, user: str) -> None:
        ans: List[str] = []
        for status in tweepy.Cursor(self.api.user_timeline, screen_name=user, tweet_mode="extended").items():
            ans.append(status.full_text)
            break
        return ans

    def frens(self, user: str) -> List[str]:
        return [x.screen_name for x in self.api.get_friends(screen_name=user)]


class Db:
    def __init__(self) -> None:
        self.conn = self._connect_rds_mysql()

    def __enter__(self) -> Db:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # TODO handle exceptions
        self.conn.commit()
        self.conn.close()

    def _connect_rds_mysql() -> MySQLConnection:
        RDS_ENDPOINT = environ["RDS_ENDPOINT"]
        RDS_USER = environ["RDS_USER"]
        RDS_PASSWORD = environ["RDS_PASSWORD"]
        RDS_PORT = environ["RDS_PORT"]
        environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"
        connect(
            host=RDS_ENDPOINT,
            user=RDS_USER,
            passwd=RDS_PASSWORD,
            port=RDS_PORT,
            database="twitter_bot",
        )

    def query(self, query: str, data=tuple()) -> List[Tuple]:
        cur = self.conn.cursor()
        cur.execute(query, data)
        ans = cur.fetchall()
        cur.close()
        return ans

if __name__ == '__main__':
    ...
    # Twitter().print_user_tweet("geoffreyhinton")
    # Twitter().make_tweet('Hello, world!')
    # print(Twitter().frens("geoffreyhinton"))
