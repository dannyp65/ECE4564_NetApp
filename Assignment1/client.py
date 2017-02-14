#!/usr/bin/env python3

"""
ECE4564: Network Application - Spring 2017
Instructor:     William O. Plymale
Assignment:     Assignment 1 - Twitter Inquirer
Date:           02/13/2017
File name:      client.py
Developer:      Team 16 - Anup Jasani, John Stradling, Kenta Yoshimura, Nhan Pham
Description:    This client application runs on Raspberry Pi 3 (Rpi)
                the client application will capture "question" tweet using Twitter API and build question payload.
                Then it sends the question payload to server Rpi via socket interface. The client app receives a answer
                payload from the server, parses it then tweet the answer on twitter
Last modify:    02/13/2017
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
# Tweepy API settings
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
    print('Parsed Through Question Tweet')

#this function generates a MD5 checksum value from string
def MD5_Encode(str):
    endata = str.encode('utf-8')
    m = hashlib.md5()
    m.update(endata)
    return m.hexdigest()

#this function receive a string and a checksum value
#it generate a new checksum value for the input string
#then checking it with the checksum to see if the transferred string is correct
def Check_Payload(str, checksum):
    compute_checksum = MD5_Encode(str)
    if checksum == compute_checksum:
        return True
    else:
        return False


class listener(StreamListener):
    def on_data(self, data):
        print('Found Question Tweet')
        tweet_data = json.loads(data)
        id_text = json.dumps(tweet_data['id'])
        user_text = json.dumps(tweet_data['user'])
        tweet_text = json.dumps(tweet_data['text'])
        parse_received_text(tweet_text, user_text)
        host = ip
        port = int(port_num)
        size = 1024
        s = None
        try:
            print('Connecting to Server')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object that use IPv4 and TCP
            s.connect((host, port))
        except socket.error as message:
            if s:
                s.close()
            print("Unable to open socket: " + str(message))
            sys.exit(1)
        print('Connected to Server')

        checksum = MD5_Encode(question)             # generate a MD5 cheksum value for the question
        tuple_data = (question, checksum)           # pack the question and checksum value into a tuple
        pickle_data = pickle.dumps(tuple_data)      # pickling the tuple
        print('Sending Question Payload to Server')
        s.send(pickle_data)                         # send pickled data to the server
        receive_pickle = s.recv(size)               # receive data from the server
        receive_data = pickle.loads(receive_pickle) # unpickling the data
        answer = receive_data[0]                    # extract the answer
        print('Payload Received\nChecking MD5 Checksum')

        #checking if the receive answer is authentic
        if(Check_Payload(receive_data[0], receive_data[1])):
            print('Checksum Verified')
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

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = listener()
    twitterStream = Stream(auth, l)
    print("Twitter Stream Listening for @team16_RPI")
    twitterStream.filter(track=['team16_RPI'])

