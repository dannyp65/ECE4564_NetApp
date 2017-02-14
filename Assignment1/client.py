#!/usr/bin/env python3

"""
A simple echo client that handles some exceptions
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
import socket
import sys
import time
import json
import pickle
import hashlib
# Tweepy settings
ckey = 'JlBGZm3es4ElEWGkBTb0DClgk'
csecret = 'uEXQ6UWbqBnlewHVWS3IZIkyjYwjIZH4CC9RlL4p4bONOp6UgK'
atoken = '831269027032997893-0QUBo1qHqWAvwqaEBmdfTHYXOZD1WVC'
asecret = 'ThaeUTqMis9MACGLuClIOYRCZcCPCcrCFC4D5Rq77WRNg'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterAPI = API(auth)

def parse_received_text(str, user):
    global ip, port_num, question, replyID
    ip = str.split(':')[0].split('#')[1]
    port_num = str.split(':')[1].split('_')[0]
    question = str.split('"')[2].split('\\')[0]
    replyID = user.split('"screen_name": "')[1].split('"')[0]
    #print(ip, port_num, question)

def MD5_Encode(str):
    endata = str.encode('utf-8')
    m = hashlib.md5()
    m.update(endata)
    return m.hexdigest()
def Check_Payload(str, checksum):
    compute_checksum = MD5_Encode(str)
    if checksum == compute_checksum:
        return True
    else:
        return False


class listener(StreamListener):
    def on_data(self, data):
        tweet_data = json.loads(data)
        tweet_write_to_file = json.dumps(tweet_data)
        id_text = json.dumps(tweet_data['id'])
        #print(id_text)
        user_text = json.dumps(tweet_data['user'])
        tweet_text = json.dumps(tweet_data['text'])
        parse_received_text(tweet_text, user_text)
        #print(replyID)
        with open('streamed_tweets.txt', 'a') as tf:
            tf.write(tweet_write_to_file)
        host = ip
        port = int(port_num)
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
        checksum = MD5_Encode(question)
        tuple_data = (question, checksum)
        pickle_data = pickle.dumps(tuple_data)
        s.send(pickle_data)
        receive_pickle = s.recv(size)
        receive_data = pickle.loads(receive_pickle)
        answer = receive_data[0]
        if(Check_Payload(receive_data[0], receive_data[1])):
            print('Answer:', answer)
            replyText = '@' + replyID + ' #"' + answer + '"'
            if len(replyText) > 140:
                replyText = replyText[0:139] + '…'
            twitterAPI.update_status(status=replyText, in_reply_to_status_id=id_text)
            print('Tweet replied')
        else:
            print('MD5 Verification Fail!')
        s.close()

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
    twitterStream = Stream(auth, l)
    print("Listening")
    twitterStream.filter(track=['team16_RPI'])


# host settings - Tweet_Ex [@username #host:port_"What is a question?"]

