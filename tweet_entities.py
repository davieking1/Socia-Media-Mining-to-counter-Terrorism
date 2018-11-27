import tweepy
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy.streaming import Stream
from unidecode import unidecode
import time
import sqlite3
import json

conn = sqlite3.connect('tweepy.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS tweepy_entities (unix REAL, tweetText TEXT, user TEXT, followers INTEGER, date TEXT, location TEXT)")
        c.execute("CREATE INDEX fast_unix ON tweepy_entities(unix)")
        c.execute("CREATE INDEX fast_tweetText ON tweepy_entities(tweetText)")
        c.execute("CREATE INDEX fast_user ON tweepy_entities(user)")
        c.execute("CREATE INDEX fast_followers ON tweepy_entities(followers)")
        c.execute("CREATE INDEX fast_date ON tweepy_entities(date)")
        c.execute("CREATE INDEX fast_location ON tweepy_entities(location)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()

global api
access_token = ""
access_token_secret = ""
consumer_key=""
consumer_key_secret=""
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api=tweepy.API(auth)

class Listener(StreamListener):
    def on_data(self,data):
        try:
            tweet = json.dumps(data)
            if not tweet['retweeted'] and 'RT @' not in tweet['text']:
                user_profile = api.get_user(tweet['user']['screen_name'])
                tweetText = unidecode(tweet['text'])
                user = tweet['user']['screen_name']
                followers = user_profile.followers_count
                data = tweet['created_at']
                location = tweet['user']['location']
                print(tweetText, user, followers, date, location)
                c.execute("INSERT INTO tweepy_entities(unix,tweetText, user, followers, date, location) VALUES(?,?,?,?,?,?)", (tweetText,user,followers,date,location))
                conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    while True:
        try:
            l = Listener()
            streamer = Stream(auth, l)
            streamer.filter(track=['USA','Douma'])
        except BaseException as e:
            print(str(e))
            time.sleep(5)


