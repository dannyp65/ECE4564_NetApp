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
import pickle

# Tweepy settings
ckey = 'tUoMh4IoOJjspbQnP6idBat8W'
csecret = 'NFIl06VPr4sIWSliAgy8dHSmPuZoTJNnPdkY4hKRAlxU1EKb0q'
atoken = '776215902224343040-jexMVewgSgJTZp3NTC5VU8RjYBvXYjy'
asecret = 'WDh56LvfK1NrNEPCZgarFzeLwvp6Pl3QAN17GtaPetiIW'


def parse_received_text(str):
    global ip, port_num, question
    ip = str.split(':')[0].split('#')[1]
    port_num = str.split(':')[1].split('_')[0]
    question = str.split('"')[2].split('\\')[0]
    print(ip, port_num, question)

class listener(StreamListener):
    def on_data(self, data):
        tweet_data = json.loads(data)
        tweet_text = json.dumps(tweet_data['text'])
        print(tweet_text)
        parse_received_text(tweet_text)
        # with open('streamed_tweets.txt', 'a') as tf:
        #     tf.write(tweet_text)
        host = ip
        port = int(port_num)
        size = 1024
        s = None
        print('IP', ip, 'PORT', port_num)
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
        data_string = pickle.dumps(question)
        s.send(data_string)
        data = s.recv(size)
        data_loaded = pickle.loads(data)
        s.close()
        print('Received:', data_loaded)
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
    twitterStream.filter(track=['#172.30.102.140:50003_'])


# host settings - Tweet_Ex [@username #host:port_"What is a question?"]

