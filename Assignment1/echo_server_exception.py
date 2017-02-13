#!/usr/bin/env python3

"""
A simple echo server that handles some exceptions
"""

import socket
import sys

host = ''
port = 50000
backlog = 5
size = 1024
s = None
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
print('Socket Create')
try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    # could not resolve
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('Ip address of ' + host + ' is ' + remote_ip)

# Connect to remote server
s.connect((remote_ip, port))

print
'Socket Connected to ' + host + ' on ip ' + remote_ip

while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        client.send(data)
    client.close()