import tweepy
import socket
import json
import json
from constants import HASHTAGS, HOST, PORT, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

class TwitterListener(tweepy.Stream):
    conn = None

    def on_data(self, data):
        try:
            processed = json.loads(data)
            tweet_text = processed['text'].encode('utf-8')
            self.conn.send(tweet_text)
        except BaseException as e:
            print("Error: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f'Socket Server is listening @ {HOST}:{PORT}')
conn, addr = s.accept()
print("Received request from: " + str(addr))
twitter_stream = TwitterListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
twitter_stream.conn = conn
twitter_stream.filter(track=HASHTAGS)
