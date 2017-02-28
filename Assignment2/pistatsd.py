#/usr/bin/env python3
"""
ECE4564: Network Application - Spring 2017
Instructor:     William O. Plymale
Assignment:     Assignment 2 - Little Brother
Date:           02/23/2017
File name:      pistatsd.py
Developer:      Team 16 - Anup Jasani, John Stradling, Kenta Yoshimura, Nhan Pham
Description:

Last modify:    02/27/2017
"""

import time
import json
import sys
import pika

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

ip_addr, virt_host, creds, routing_keys = get_args()
last_idle = last_total = 0
readonce = True
user, password = creds.split(':')

print("Trying to Connect to Message Broker")
try:
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(ip_addr,
                                           5672,
                                           virt_host,
                                           credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='pi_utilization',
                             type='direct')
except:
    print("Connection Error!")
    sys.exit()

print("Connected to Message Broker")    
print("Starting", routing_keys)
print("..................................................................")
while 1:
    print("Calculating CPU Utilization")
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = (1.0 - idle_delta / total_delta)
    print("Finished Calculating CPU Utilization")
    if readonce == True:
        print("Calculating Network Throughput")
        net = open('/proc/net/dev')
        netfield = net.read().split()
        last_wlan0R = float(netfield[21])
        last_wlan0T = float(netfield[29])
        last_loR = float(netfield[38])
        last_loT = float(netfield[46])
        last_eth0R = float(netfield[55])
        last_eth0T = float(netfield[63])
        net.close()
        time.sleep(1)
        net = open('/proc/net/dev')
        netfield = net.read().split()
        wlan0R = float(netfield[21])
        wlan0T = float(netfield[29])
        loR = float(netfield[38])
        loT = float(netfield[46])
        eth0R = float(netfield[55])
        eth0T = float(netfield[63])
        net.close()
        wlan0R_delta, wlan0T_delta = wlan0R - last_wlan0R, wlan0T - last_wlan0T
        loR_delta, loT_delta = loR - last_loR, loT - last_loT
        eth0R_delta, eth0T_delta = eth0R - last_eth0R, eth0T - last_eth0T
        readonce = False
    else:
        print("Calculating Network Throughput")
        time.sleep(1)
        net = open('/proc/net/dev')
        netfield = net.read().split()
        wlan0R = float(netfield[21])
        wlan0T = float(netfield[29])
        loR = float(netfield[38])
        loT = float(netfield[46])
        eth0R = float(netfield[55])
        eth0T = float(netfield[63])
        net.close()
        wlan0R_delta, wlan0T_delta = wlan0R - last_wlan0R, wlan0T - last_wlan0T
        loR_delta, loT_delta = loR - last_loR, loT - last_loT
        eth0R_delta, eth0T_delta = eth0R - last_eth0R, eth0T - last_eth0T

    last_wlan0R, last_wlan0T = wlan0R, wlan0T
    last_loR, last_loT = loR, loT
    last_eth0R, last_eth0T = eth0R, eth0T
    print("Finished Calculating Network Throughput")
    print("Creating JSON Object")
    message = json.dumps({"net": { "lo": { "rx": loR_delta, "tx": loT_delta }, "wlan0": { "rx": wlan0R, "tx": wlan0T },
                         "eth0": { "rx": eth0R_delta, "tx": eth0T_delta } }, "cpu": utilisation } , sort_keys = False, indent = 4)
    print("Sending JSON Object to Message Broker")
    channel.basic_publish(exchange='pi_utilization',
                          routing_key=routing_keys,
                          body=message)
    print("Finished Sending to Message Broker")
    print("..................................................................")
connection.close()
