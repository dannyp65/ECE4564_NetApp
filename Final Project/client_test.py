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


# Function for command line arguments
def get_args():
    opt_in_opt = "ERROR: cannot take another opt flag as a parameter"
    cmd_args = sys.argv
    cmd_len = len(cmd_args)
    p_check, a_check, c_check, s_check, r_check = False, False, False, False, False
    p_opt, a_opt, c_opt, s_opt, r_opt = '', '', '', '', ''
    for i in range(1, cmd_len):
        if cmd_args[i] == p_opt or cmd_args[i] == a_opt or cmd_args[i] == c_opt or cmd_args[i] == s_opt or cmd_args[i] == r_opt:
            continue
        if cmd_args[i] == '-p':
            try:
                p_opt = cmd_args[i + 1]  # raise out of range
                if p_opt == '-p' or p_opt == '-a' or p_opt == '-c' or p_opt == '-s' or p_opt == '-r':
                    print(opt_in_opt, '1')
                    sys.exit()  # raise SystemExit
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no Port given")
                raise SystemExit
            p_check = True
        elif cmd_args[i] == '-a':
            try:
                a_opt = cmd_args[i + 1]  # raise out of range
                if a_opt == '-p' or a_opt == '-a' or a_opt == '-c' or a_opt == '-s' or a_opt == '-r':
                    print(opt_in_opt, '1')
                    sys.exit()  # raise SystemExit
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no Activity given")
                raise SystemExit
            a_check = True
        elif cmd_args[i] == '-s':
            try:
                s_opt = cmd_args[i + 1]
                if s_opt == '-p' or s_opt == '-a' or s_opt == '-c' or s_opt == '-s' or s_opt == '-r':
                    print(opt_in_opt, '2')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no State given")
                raise SystemExit
            s_check = True
        elif cmd_args[i] == '-c':
            try:
                c_opt = cmd_args[i + 1]
                if c_opt == '-p' or c_opt == '-a' or c_opt == '-c' or c_opt == '-s' or c_opt == '-r':
                    print(opt_in_opt, '3')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no City given")
                raise SystemExit
            c_check = True
        elif cmd_args[i] == '-r':
            try:
                r_opt = cmd_args[i + 1]
                if r_opt == '-p' or r_opt == '-a' or r_opt == '-c' or r_opt == '-s' or r_opt == '-r':
                    print(opt_in_opt, '4')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no Radius given")
                raise SystemExit
            r_check = True
        elif cmd_args[i].startswith('-'):
            print("ERROR: incorrect opt flag", cmd_args[i])
            sys.exit()
        else:
            print("ERROR: ELSE", cmd_args[i])
            sys.exit()
    if p_check and a_check and c_check and s_check and r_check:
        return p_opt, a_opt, c_opt, s_opt, r_opt
    else:
        print("ERROR: all parameters need to be set")
        sys.exit()


# this function generates a MD5 checksum value from string
def MD5_Encode(str):
    endata = str.encode('utf-8')
    m = hashlib.md5()
    m.update(endata)
    return m.hexdigest()


# this function receives a string and a checksum value
# it generates a new checksum value for the input string
# then checking it with the checksum to see if the transferred string is correct
def Check_Payload(str, checksum):
    compute_checksum = MD5_Encode(str)
    if checksum == compute_checksum:
        return True
    else:
        return False


def main():
    # gets commandline arguments
    addr_port, activity, city, state, radius = get_args()
    print(addr_port, activity, city, state, radius, "\n")
    host = addr_port.split(':')[0]
    port = int(addr_port.split(':')[1])
    size = 4096
    s = None
    try:
        print('Connecting to Server')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object that use IPv4 and TCP
        s.connect((host, port))
    except socket.error as message:
        if s:
            s.close()
        print("Unable to open socket: " + str(message))
        sys.exit(1)
    print('Connected to Server')

    data_str = ','.join((activity, city, state, radius))
    checksum = MD5_Encode(data_str)  # generate a MD5 cheksum value for the question
    tuple_data = (data_str, checksum)  # pack the question and checksum value into a tuple
    pickle_data = pickle.dumps(tuple_data)  # pickling the tuple
    print('Sending Parameters to Server')
    s.send(pickle_data)  # send pickled data to the server

    print('Sent and Waiting to Receive')
    recv_pickle = s.recv(size)  # receive data from the server
    recv_data = pickle.loads(recv_pickle)  # unpickling the data
    print('Payload Received\nChecking MD5 Checksum')

    # checking if the receive answer is authentic
    if (Check_Payload(recv_data[0], recv_data[1])):
        print('Checksum Verified\n')
        places = recv_data[0].split('[?]')[0].split('[!]')
        weather_stats = recv_data[0].split('[?]')[1].split('[!]')
        c = 1
        print("Found %d Places:" % (len(places)))
        for x in places:
            print("%d." % c, x)
            c += 1
        print("-----\nTemp(Min, Current, Max): {0}{5}F, {1}{5}F, {2}{5}F \nWind Speed: {3} \nClouds: {4}\n-----\n".format(weather_stats[1], weather_stats[0], weather_stats[2], weather_stats[3], weather_stats[4], chr(176)))
    else:
        print('MD5 Verification Fail!')
    s.close()
    return True


if __name__ == '__main__':  # runs the application
    main()
