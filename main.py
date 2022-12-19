from __future__ import annotations

from functools import wraps
from os import environ
from typing import *  # type: ignore

import tweepy
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection

ML_PPL_FILE = "ml-ppl.txt"

_DEBUG = True

def _print(*args, **kwargs) -> None:
    if _DEBUG:
        print(*args, **kwargs)


def _debug_func(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        _print("CALLING", func.__qualname__)
        ans = func(*args, **kwargs)
        _print(f"{func.__qualname__}", "OUTPUT", ans)
        return ans

    return wrapper


def _debug(cls) -> type:
    for key, value in vars(cls).items():
        if callable(value):
            setattr(cls, key, _debug_func(value))
            continue
    return cls

@_debug
class Twitter:
    """
    Twitter().make_tweet('Hello, world!')
    Twitter().frens("geoffreyhinton")
    """
    def __init__(self):
        self.api = self.get_twitter_api()
        self.db = Database()

    def get_twitter_api(self) -> tweepy.APIz:
        consumer_key = environ["TWITTER_BOT_API_KEY"]
        consumer_secret = environ["TWITTER_BOT_API_KEY_SECRET"]
        access_token = environ["TWITTER_BOT_ACCESS_TOKEN"]
        access_token_secret = environ["TWITTER_BOT_ACCESS_TOKEN_SECRET"]
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def make_tweet(self, tweet: str) -> None:
        self.api.update_status(tweet)

    def get_tweets(self, user: str) -> None:
        ans: List[str] = []
        for status in tweepy.Cursor(self.api.user_timeline, screen_name=user, tweet_mode="extended").items():
            ans.append(status.full_text)
            if _DEBUG:
                break
        return ans

    def frens(self, user: str) -> List[str]:
        return [x.screen_name for x in self.api.get_friends(screen_name=user)]

    def insert_users_tweets_into_db(self, user: str) -> None:
        tweets = self.get_tweets(user)
        for tweet in tweets:
            with self.db as db:
                db.insert_tweet_into_tweets_table(user, tweet)
                if _DEBUG:
                    break

    def get_users(self) -> List[str]:
        with open(ML_PPL_FILE, 'r') as f:
            return [x.strip() for x in f.readlines()]

    def populate_db_with_users_tweets(self, users: List[str]) -> None:
        for user in users:
            self.insert_users_tweets_into_db(user)
            if _DEBUG:
                break

@_debug
class Database:
    def __init__(self) -> None:
        self.conn = self._connect_rds_mysql()

    def __enter__(self) -> Database:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # TODO handle exceptions
        self.conn.commit()
        self.conn.close()

    def _connect_rds_mysql(self) -> MySQLConnection:
        RDS_ENDPOINT = environ["RDS_ENDPOINT"]
        RDS_USER = environ["RDS_USER"]
        RDS_PASSWORD = environ["RDS_PASSWORD"]
        RDS_PORT = environ["RDS_PORT"]
        environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"
        return connect(
            host=RDS_ENDPOINT,
            user=RDS_USER,
            passwd=RDS_PASSWORD,
            port=RDS_PORT,
            database="twitter_bot",
        )

    def insert_tweet_into_tweets_table(self, user: str, tweet: str) -> None:
        print(1)
        cur = self.conn.cursor()
        print(cur)
        cur.execute("""
        INSERT IGNORE INTO tweets(username, tweet_text)
        VALUES (%s, %s)
        """, (user, tweet))
        cur.close()

    def query(self, query: str, data=tuple()) -> List[Tuple]:
        cur = self.conn.cursor()
        cur.execute(query, data)
        ans = cur.fetchall()
        cur.close()
        return ans


def write_geoffrey_hinton_friend_graph() -> None:
    # TODO to get more people do friends of friends...
    #      you'll want to set() the results when you do that!
    with open(ML_PPL_FILE, 'w') as f:
        f.write("geoffreyhinton\n")
        f.write('\n'.join(Twitter().frens("geoffreyhinton")))
        f.write('\n')

def populate_db_with_users_tweets() -> None:
    t = Twitter()
    t.populate_db_with_users_tweets(t.get_users())

if __name__ == '__main__':
    # write_geoffrey_hinton_friend_graph()
    populate_db_with_users_tweets()
