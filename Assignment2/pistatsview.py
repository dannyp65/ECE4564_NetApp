#/usr/bin/env python3
"""
ECE4564: Network Application - Spring 2017
Instructor:     William O. Plymale
Assignment:     Assignment 2 - Little Brother
Date:           02/23/2017
File name:      pistatsview.py
Developer:      Team 16 - Anup Jasani, John Stradling, Kenta Yoshimura, Nhan Pham
Description:

Last modify:    02/23/2017
"""

import pika
import sys
import pymongo
from pymongo import MongoClient
import pprint
import RPi.GPIO as GPIO
import time
import json


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

def threshold_RGB(curr_cpu):
    #turn off all LEDs
    GPIO.output(24,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
    global cpu_hi, cpu_lo
    diff = cpu_hi - cpu_lo
    cpu_50 = cpu_lo + diff/2.0
    cpu_25 = cpu_lo + diff/4.0
    if curr_cpu <= cpu_25:
        #turn on green
        print('LED is green')
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
    elif curr_cpu > cpu_25 and curr_cpu < cpu_50:
        #turn on yellow = green + red
        print('LED is yellow')
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
    elif curr_cpu >= cpu_50:
        #turn on red
        print('LED is red')
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)

print("Starting Monitor RPi")
ip_addr, virt_host, creds, routing_key = get_args()
user, password = creds.split(':')

# ****RabbitMQ START
credentials = pika.PlainCredentials(user, password)
parameters = pika.ConnectionParameters(ip_addr, 5672, virt_host, credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='pi_utilization',
                             type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='pi_utilization',
                        queue=queue_name,
                        routing_key=routing_key)
client = MongoClient()
db = client.database_1  #nothing actually done until first doc inserted
collection = db.collection_1
db.collection_1.drop()

#setup all GPIO ports
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

cpu_hi = 0
lo_rx_hi = lo_tx_hi = eth_rx_hi = eth_tx_hi = wlan_rx_hi = wlan_tx_hi = 0.0
cpu_lo = 1
lo_rx_lo = lo_tx_lo = eth_rx_lo = eth_tx_lo = wlan_rx_lo = wlan_tx_lo = 50000000000000000000000.0

def callback(ch, method, properties, body):
    global cpu_hi, lo_rx_hi, lo_tx_hi, eth_rx_hi, eth_tx_hi, wlan_rx_hi, wlan_tx_hi
    global cpu_lo, lo_rx_lo, lo_tx_lo, eth_rx_lo, eth_tx_lo, wlan_rx_lo, wlan_tx_lo
    post = json.loads(body.decode('utf-8'))
    db.collection_1.insert_one(post)    #inserts new JSON and returns it's ID
    for p in db.collection_1.find():
        if p['cpu'] > cpu_hi: cpu_hi = p['cpu']
        if p['cpu'] < cpu_lo: cpu_lo = p['cpu']
        if post['net']['lo']['rx'] > lo_rx_hi: lo_rx_hi = post['net']['lo']['rx']
        if post['net']['lo']['rx'] < lo_rx_lo: lo_rx_lo = post['net']['lo']['rx']
        if post['net']['lo']['tx'] > lo_tx_hi: lo_tx_hi = post['net']['lo']['tx']
        if post['net']['lo']['tx'] < lo_tx_lo: lo_tx_lo = post['net']['lo']['tx']

        if post['net']['eth0']['rx'] > eth_rx_hi: eth_rx_hi = post['net']['eth0']['rx']
        if post['net']['eth0']['rx'] < eth_rx_lo: eth_rx_lo = post['net']['eth0']['rx']
        if post['net']['eth0']['tx'] > eth_tx_hi: eth_tx_hi = post['net']['eth0']['tx']
        if post['net']['eth0']['tx'] < eth_tx_lo: eth_tx_lo = post['net']['eth0']['tx']

        if post['net']['wlan0']['rx'] > wlan_rx_hi: wlan_rx_hi = post['net']['wlan0']['rx']
        if post['net']['wlan0']['rx'] < wlan_rx_lo: wlan_rx_lo = post['net']['wlan0']['rx']
        if post['net']['wlan0']['tx'] > wlan_tx_hi: wlan_tx_hi = post['net']['wlan0']['tx']
        if post['net']['wlan0']['tx'] < wlan_tx_lo: wlan_tx_lo = post['net']['wlan0']['tx']
    print("%s:\ncpu: %s [Hi: %s, Lo: %s]\nlo: rx=%s B/s [Hi: %s, Lo:%s], tx=%s B/s [Hi: %s, Lo:%s]\neth0: rx=%s B/s [Hi: %s, Lo:%s], tx=%s B/s [Hi: %s, Lo:%s]\nwlan0: rx=%s B/s [Hi: %s, Lo:%s], tx=%s B/s [Hi: %s, Lo:%s]\n"
          % (method.routing_key, post['cpu'], cpu_hi, cpu_lo, post['net']['lo']['rx'], lo_rx_hi, lo_rx_lo, post['net']['lo']['tx'], lo_tx_hi, lo_tx_lo,
             post['net']['eth0']['rx'], eth_rx_hi, eth_rx_lo, post['net']['eth0']['tx'], eth_tx_hi, eth_tx_lo,
             post['net']['wlan0']['rx'], wlan_rx_hi, wlan_rx_lo, post['net']['wlan0']['tx'], wlan_tx_hi, wlan_tx_lo))
    threshold_RGB(post['cpu'])

channel.basic_consume(callback,
                        queue=queue_name,
                        no_ack=True)
channel.start_consuming()
#****RabbitMQ END
