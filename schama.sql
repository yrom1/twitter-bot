-- Version 0: users and tweets table
-- Version 1:
--    * denominalized the table (remove users table)
--    * drop the 4000 char limit to 280 (this is a future ryan problem)
--      this lets me use tweet_text as primary key, I wonder if Twitter
--      is going to have this problem, I guess they'll just hash it

CREATE DATABASE IF NOT EXISTS twitter_bot;

USE twitter_bot;

CREATE TABLE IF NOT EXISTS tweets (
  username VARCHAR(255),
  tweet_text VARCHAR(280) NOT NULL,
  PRIMARY KEY (username, tweet_text)
);
