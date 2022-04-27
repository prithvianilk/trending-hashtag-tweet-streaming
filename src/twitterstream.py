import tweepy
import socket
import json

consumer_key="QZtm1FzgtGvybrkNDeKtiw8O2"
consumer_secret ="q1zE545GzdrVtfks1Rs7JYiN671LOnsrygRDdWkKlAvRJBDPBG"
access_token="1379074550210514944-FEkutfsE430HLEbPuKRskmOuCWbgXn"
access_secret="J5BMlIOM50M2fFvR38mYvssLlzCpPGGnCuoOXhJaDYL2u"
HOST = "localhost"
PORT = 9008

class MyListener(tweepy.Stream):

    def setCon(self,conn):
        self.conn = conn

    def on_data(self, data):
        try:
            processed = json.loads(data)
            tweettext = processed['text'].encode('utf-8')
            self.conn.send(tweettext)
        except BaseException as e:
            print("Error: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print('Socket is ready')
s.listen(1)
print('Socket listening')
c_socket, addr = s.accept()
print("Received request from: " + str(addr))
twitter_stream = MyListener(consumer_key, consumer_secret, access_token, access_secret)
twitter_stream.setCon(c_socket)
twitter_stream.filter(track=['#ElonMusk',"#Ukraine","#IPL","#Valorant","#KGFChapter2"])
