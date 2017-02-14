#!/usr/bin/env python3

"""
A simple echo server that handles some exceptions
"""

import socket
import sys
import wolframalpha
import pickle
import hashlib

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

host = ''
port = 50003
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
    pickled_data = wclient.recv(size)
    received_data = pickle.loads(pickled_data)
    question = received_data[0]
    receive_checksum = received_data[1]

    #if check1 == client1:

    if Check_Payload(question,receive_checksum):
        appid = "27TG8H-VEQ8L3WAJ5"
        client = wolframalpha.Client(appid)
        res = client.query(question)
        answer = next(res.results).text
        print(answer)
        new_checksum = MD5_Encode(answer)
        tuple_data = (answer, new_checksum)
        data_send = pickle.dumps(tuple_data)
        wclient.send(data_send)
    else:
        wclient.send(b'MD5 Verification Fail!')
        #print (data_string)
    wclient.close()