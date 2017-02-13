#!/usr/bin/env python3

"""
A simple echo client that handles some exceptions
"""

import socket
import sys
import pickle
import hashlib

host = 'localhost'
port = 50000
size = 1024
s = None
storedval = "How far away is Pluto"
storefval1 = '123456789'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
#except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print ("Unable to open socket: " + str(message))
    sys.exit(1)
"""""
m = hashlib.md5()
m.update(storedval.encode('utf-8'))
m.hexdigest()
print(m)
"""""

data_string = pickle.dumps(storedval)
#store1 = pickle.dumps(m)
s.send(data_string)
#s.send(store1)
data = s.recv(size)
#print(data)
data_loaded = pickle.loads(data)
s.close()
print ('Received:', data_loaded)
