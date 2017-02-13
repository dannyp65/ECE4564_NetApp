#!/usr/bin/env python3

"""
ECE4564: Network Application - Spring 2017
Instructor:     William O. Plymale
Assignment:     Assignment 1 - twitter Inquirer
Date:           02/13/2017
File name:      server.py
Developer:      Team 16 - Anup Jasani, John Stradling, Kenta Yoshimura, Nhan Pham
Description:    This server application runs on Raspberry Pi 3 (Rpi)
                the server will receive question payload from client Rpi then parses the question payload
                and sends the question to WolframAlpha engine via API call.
                After received answer from WolframAlpha engine, the server build answers payload
                and sends it back to the client via socket interface.
Last modify:    02/13/2017
"""

import socket
import sys
import wolframalpha
import pickle
import hashlib

#this function generates a MD5 checksum value from string
def MD5_Encode(str):
    endata = str.encode('utf-8')
    m = hashlib.md5()
    m.update(endata)
    return m.hexdigest()
# end MD5_Encode function

#this function receive a string and a checksum value
#it generate a new checksum value for the input string
#then checking it with the checksum to see if the transferred string is correct
def Check_Payload(str, checksum):
    compute_checksum = MD5_Encode(str)
    if checksum == compute_checksum:
        return True
    else:
        return False
# end Check_Payload function

host = ''
port = 50000
backlog = 5
size = 1024
s = None
errorM = "Error: Data has been corrupted.  Incorrect md5 value!"
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object that use IPv4 and TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((host,port))
    s.listen(backlog)
except socket.error as message: #error handling
    if s:
        s.close()
    print ("Could not open socket: " + str(message))
    sys.exit(1)

while 1:
    wclient, address = s.accept()               # accept request from a client
    pickled_data = wclient.recv(size)           # received a pickled data
    received_data = pickle.loads(pickled_data)  # unpickling data

    # store the question and checksum value from received tuple into variables
    question = received_data[0]
    receive_checksum = received_data[1]


    if Check_Payload(question,receive_checksum):# checking if the the checksum to see if the information is correct
        #connect to wolfram server
        appid = "27TG8H-VEQ8L3WAJ5"
        client = wolframalpha.Client(appid)

        res = client.query(question)            # send the question to wolfram
        answer = next(res.results).text         # receive the answer
        print(answer)

        new_checksum = MD5_Encode(answer)       # generate a checksum for the answer
        tuple_data = (answer, new_checksum)     # pack answer and checksum into tuple
        data_send = pickle.dumps(tuple_data)    # pickle the data
        wclient.send(data_send)                 # send data back to the client

    else: # if checksum not correct, send an error message to the client
        wclient.send(b'MD5 Verification Fail!')

    # close the connection with client
    wclient.close()