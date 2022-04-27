import socket
import sys
import requests
import requests_oauthlib
import json


TCP_IP = "localhost"
TCP_PORT = 9009

API_KEY="QZtm1FzgtGvybrkNDeKtiw8O2"
API_SECRET_KEY ="q1zE545GzdrVtfks1Rs7JYiN671LOnsrygRDdWkKlAvRJBDPBG"
ACCESS_TOKEN="1379074550210514944-FEkutfsE430HLEbPuKRskmOuCWbgXn"
ACCESS_TOKEN_SECRET="J5BMlIOM50M2fFvR38mYvssLlzCpPGGnCuoOXhJaDYL2u"

TWITTER_URL = "https://stream.twitter.com/1.1/statuses/filter.json"
QUERY_DATA = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
QUERY_URL = TWITTER_URL + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in QUERY_DATA])

class TwitterStreamScraper:
    def __init__(self):
        self.auth = requests_oauthlib.OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))

    def listen(self):
        self.s.listen(1)
        conn, _ = self.s.accept()
        print("TCP Connection Established")
        resp = self.get_tweets_data()
        self.send_tweets_to_spark(resp, conn)
    
    def get_tweets_data(self):
        response = requests.get(QUERY_URL, auth=self.auth, stream=True)
        return response

    def send_tweets_to_spark(self, http_resp, tcp_connection):
        for line in http_resp.iter_lines():
            try:
                full_tweet = json.loads(line)
                tweet_text = full_tweet['text']
                print(tweet_text)
                tcp_connection.send(tweet_text.encode())
            except:
                error = sys.exc_info()[0]
                print("Error: %s" % error)

scaper = TwitterStreamScraper()
scaper.listen()