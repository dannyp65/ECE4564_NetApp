#!/usr/bin/env python3

"""
A simple echo server that handles some exceptions
"""

import socket
import sys
import wolframalpha
import pickle
import hashlib

host = '172.30.45.91'
port = 50000
backlog = 5
size = 1024
s = None
errorM = "Error: Data has been corrupted.  Incorrect md5 value!"
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((host,port))
    s.listen(backlog)
except socket.error as message:
    if s:
        s.close()
    print ("Could not open socket: " + str(message))
    sys.exit(1)

while 1:
    wclient, address = s.accept()
    data = wclient.recv(size)
    data_loaded = pickle.loads(data)
    """""
    #attempting checksum************
    check1 = hashlib.md5()
    check1.update(data_loaded)
    check1.hexdigest()
    """""
    #if check1 == client1:

    if data:
       # print (data_loaded)

        input = data_loaded

        appid = "27TG8H-VEQ8L3WAJ5"
        client = wolframalpha.Client(appid)

        res = client.query(input)
        answer = next(res.results).text
        print(answer)
        data_string = pickle.dumps(answer)

    wclient.send(data_string)
        #print (data_string)
    wclient.close()