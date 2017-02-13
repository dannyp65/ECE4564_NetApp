#!/usr/bin/env python3

"""
A simple echo client that handles some exceptions
"""

import socket
import sys


host = '192.168.1.108'
port = 50000
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
#except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print ("Unable to open socket: " + str(message))
    sys.exit(1)
s.send(b'Hello, world')
data = s.recv(size)
s.close()
print ('Received:', data)