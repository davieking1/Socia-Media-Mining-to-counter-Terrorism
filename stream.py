#-*-coding: UTF-8-*-
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

CONSUMER_KEY = ""
CONSUMER_SECRET=""
ACCESS_TOKEN =""
ACCESS_TOKEN_SECRET = ""

class stdoutListener(StreamListener):

    def on_data(self,data):
        try:
            print data
            savefile=open("twitter.txt", "a")
            savefile.write(data)
            savefile.write("\n")
            savefile.close()
            return True
        except BaseException as e:
            print("Failed on_data: %s" % str(e))
            time.sleep(5)

    def on_error(self,status):
        print(status)
if __name__ == '__main__':
    L = stdoutListener()
    auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth,L)
    stream.filter(track=["#syria","#russia", "#USA","#Douma","Trump"])
