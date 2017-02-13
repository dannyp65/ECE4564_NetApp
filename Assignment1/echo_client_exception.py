#!/usr/bin/env python3

"""
A simple echo client that handles some exceptions
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import socket
import sys
import time
import json

# Tweepy settings
ckey = 'zH3dR9T52kBtDRsAOPEMKfqoB'
csecret = 'vvI6A8f48yfPLUHhOptPAfajhZWO0gyHzTNyxoJabjkKcffRuV'
atoken = '315653672-OfKEIswzpVhf6Hbsa3kvg43Li6aDSI2rpykZiTGQ'
asecret = 'D7c7IX6nJsj2WpJ4SXRnT7HjkV3TTYjCUUVCJWw0JlOly'
question = ''
ip = ''
port = 0

def parse_received_text(str):
    ip = str.split(':')[0].split('#')[1]
    port = str.split(':')[1].split('_')[0]

    print(ip, port)

class listener(StreamListener):
    def on_data(self, data):
        tweet_data = json.loads(data)
        tweet_text = json.dumps(tweet_data['text'])
        print(tweet_text)
        parse_received_text(tweet_text)
        with open('streamed_tweets.txt', 'a') as tf:
            tf.write(tweet_text)
        return True
        # try:
        #     print("Found Data")
        #     print(data)
        #     return True
        # except BaseException as e:
        #     print('Failed onData,', str(e))
        #     time.sleep(5)

    def on_error(self, status):
        # if status == 420:
        #     print('Exceeded number of attempts to connect. Disconnecting stream.')
        #     print(status)
        #     return False
        print(status)

if __name__ == '__main__':
    l = listener()
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitterStream = Stream(auth, l)
    print("Listening")
    twitterStream.filter(track=['#172.30.24.5:50002_'])

'''
# host settings - Tweet_Ex [@username #host:port_"What is a question?"]
host = '172.30.24.5'
port = 50002
size = 1024
s = None

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
# except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print("Unable to open socket: " + str(message))
    sys.exit(1)
print('Connected to host')
s.send(b'Hello, world')
data = s.recv(size)
s.close()
print('Received:', data)
'''
