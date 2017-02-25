#!/usr/bin/python3
# !/usr/bin/env python3

"""
ECE4564: Network Application - Spring 2017
Instructor:     William O. Plymale
Assignment:     Assignment 2 - Little Brother
Date:           02/23/2017
File name:      client.py
Developer:      Team 16 - Anup Jasani, John Stradling, Kenta Yoshimura, Nhan Pham
Description:

Last modify:    02/23/2017
"""

import sys
import time


def get_args():
    opt_in_opt = "ERROR: cannot take another opt flag as a parameter"
    cmd_args = sys.argv
    cmd_len = len(cmd_args)
    b_check, p_check, c_check, k_check = False, False, False, False
    p_opt, c_opt, b_opt, k_opt = '/', 'guest:password', '', ''
    for i in range(1, cmd_len):
        if cmd_args[i] == b_opt or cmd_args[i] == p_opt or cmd_args[i] == c_opt or cmd_args[i] == k_opt:
            continue
        if cmd_args[i] == '-b':
            try:
                b_opt = cmd_args[i + 1]  # raise out of range
                if b_opt == '-b' or b_opt == '-p' or b_opt == '-c' or b_opt == '-k':
                    print(opt_in_opt, '1')
                    sys.exit()  # raise SystemExit
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no IP address given")
                raise SystemExit
            b_check = True
        elif cmd_args[i] == '-p':
            try:
                p_opt = cmd_args[i + 1]
                if p_opt == '-b' or p_opt == '-p' or p_opt == '-c' or p_opt == '-k':
                    print(opt_in_opt, '2')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no virtual host given")
                raise SystemExit
            p_check = True
        elif cmd_args[i] == '-c':
            try:
                c_opt = cmd_args[i + 1]
                if c_opt == '-b' or c_opt == '-p' or c_opt == '-c' or c_opt == '-k':
                    print(opt_in_opt, '3')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no login credentials given")
                raise SystemExit
            if ':' not in c_opt:
                print("ERROR: login credential format is incorrect")
                raise SystemExit
            c_check = True
        elif cmd_args[i] == '-k':
            try:
                k_opt = cmd_args[i + 1]
                if k_opt == '-b' or k_opt == '-p' or k_opt == '-c' or k_opt == '-k':
                    print(opt_in_opt, '4')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no routing key given")
                raise SystemExit
            k_check = True
        elif cmd_args[i].startswith('-'):
            print("ERROR: incorrect opt flag")
            sys.exit()
        else:
            print("ERROR: ELSE", cmd_args[i])
            sys.exit()
    if b_opt != '' and k_opt != '':
        return b_opt, p_opt, c_opt, k_opt
    else:
        print("ERROR: parameters -b and -k need to be set")
        sys.exit()


def output_data(host, arr1, arr2):
    s = host + ":\n" + arr2[0] + ": " + str(arr2[1]) + "\n" + arr1[1] + ": " + arr1[2] + "=" + str(
        arr1[3]) + " B/s " + ", " + arr1[4] + "=" + str(arr1[5]) + " B/s \n" + arr1[11] + ": " + arr1[12] + "=" + str(
        arr1[13]) + " B/s " + ", " + arr1[14] + "=" + str(arr1[15]) + " B/s \n" + arr1[6] + ": " + arr1[7] + "=" + str(
        arr1[8]) + " B/s " + ", " + arr1[9] + "=" + str(arr1[10]) + " B/s "
    print(s)


if __name__ == '__main__':
    ip_addr, virt_host, creds, routing_key = get_args()
    print('Info:\t', ip_addr, virt_host, creds, routing_key)
    user, password = creds.split(':')
    arr_net = ["net", "lo", "rx", 0, "tx", 0, "wlan0", "rx", 708, "tx", 1192, "eth0", "rx", 0, "tx", 0]
    arr_cpu = ["cpu", 0.2771314211797171]
    output_data(virt_host, arr_net, arr_cpu)
