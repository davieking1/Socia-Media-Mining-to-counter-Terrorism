import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy.streaming import Stream
from textblob import TextBlob
import json
import time
from unidecode import unidecode
import sqlite3

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS entries(unix REAL, tweet TEXT, user TEXT, date TEXT, location TEXT)")
        c.execute("CREATE INDEX fast_unix ON entries(unix)")
        c.execute("CREATE INDEX fast_tweet ON entries(tweet)")
        c.execute("CREATE INDEX fast_user ON entries(user)")
        c.execute("CREATE INDEX fast_date ON entries(date)")
        c.execute("CREATE INDEX fast_location ON entries(location)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()


CONSUMER_KEY = "3LcqBI1plPu4nOpnON9dx1TTp"
CONSUMER_SECRET = "gmEfPaOqPEWIsJMl0s5Fzi8byOMJTsExG5152ucO4zmU0BNXo8"
ACCESS_TOKEN = "3261168619-XVzQbOT5G9ePvbGuaFDYVgu69nuEMSb9IHuwdhE"
ACCESS_TOKEN_SECRET = "HErirtoqwt2Zcfh9mv843XkqZHNlf79eyZFiKqilc1fVt"

class listener(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            if not data['retweeted'] and 'RT @' not in data['text']:
                user_profile = api.get_user(data['user']['screen_name'])
                tweet = unidecode(data['text'])
                time_ms = data['timestamp_ms']
                user = data['user']['screen_name']
                date = data['created_at']
                location = data['user']['location']
                print(time_ms, tweet, user, date, location)
                c.execute("INSERT INTO entries (unix, tweet, user, date, location) VALUES (?, ?, ?)",
                    (time_ms, tweet, user, date, location))
                conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)



    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    while True:
        try:
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            l = listener()
            streamer = Stream(auth, l)
            streamer.filter(track=['USA', 'Syria', 'Russia', 'ISIS', 'Assad'])
        except BaseException as e:
            print(str(e))
            time.sleep(5)

