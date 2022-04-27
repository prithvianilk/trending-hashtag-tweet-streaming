# # import tweepy
# from tweepy import Stream
# # from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
import socket
import json


consumer_key="QZtm1FzgtGvybrkNDeKtiw8O2"
consumer_secret ="q1zE545GzdrVtfks1Rs7JYiN671LOnsrygRDdWkKlAvRJBDPBG"
access_token="1379074550210514944-FEkutfsE430HLEbPuKRskmOuCWbgXn"
access_secret="J5BMlIOM50M2fFvR38mYvssLlzCpPGGnCuoOXhJaDYL2u"

# auth = tweepy.OAuthHandler(API_Key,API_Secret_Key)
# auth.set_access_token(Access_Token, Access_Token_Secret)
#
# api = tweepy.API(auth,wait_on_rate_limit=True)
#
# try:
#   api.verify_credentials()
#   print("Success")
# except Exception as e:
#   print(e)
#   exit()



import tweepy

class MyListener(tweepy.Stream):

    def setCon(self,conn):
        self.conn = conn
    def on_data(self, data):
        try:
            processed = json.loads(data)
            tweettext=processed['text']
            self.conn.send("tweettext".encode())
            print("Fetched: ",tweettext)
        except BaseException as e:
            print("Error(on data): %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True



# class SL(tweepy.Stream):
#     def on_data(self,data,con):
#
#         tcp_connection.send(status.text.encode())



s = socket.socket()
host = "localhost"
port = 9008
s.bind((host, port))
print('Socket is ready')
# server (local machine) listens for connections
s.listen(4)
print('Socket listening')
# return the socket and the address on the other side of the connection (client side)
c_socket, addr = s.accept()

print("Received request from: " + str(addr))
# select here the keyword for the tweet data

twitter_stream = MyListener(consumer_key, consumer_secret, access_token, access_secret)
twitter_stream.setCon(c_socket)

twitter_stream.filter(track=['#ElonMusk',"#Ukraine","#IPL","#Valorant","#KGFChapter2"])

