#/usr/bin/env python3
import requests
import json
from twilio.rest import TwilioRestClient
import datetime
import sys
import pygame
import RPi.GPIO as GPIO

now = datetime.datetime.now()
def get_args():
    opt_in_opt = "ERROR: cannot take another opt flag as a parameter"
    cmd_args = sys.argv
    cmd_len = len(cmd_args)
    for i in range(1, cmd_len):


def playASound():
    pygame.mixer.init()
    pygame.mixer.music.load('Fart.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
      continue

def sendMess(mess, num):
    tonum = '+1' + num
    twilio_sid = "AC3fc819a1fe2f836b25e54e0ef47ba23d"
    twilio_token = "52a06091ff97cdc10f3af0f6790c9daf"
    client = TwilioRestClient(twilio_sid, twilio_token)
    message = client.messages.create(to=tonum, from_="+18045523194",
                                     body=mess)

def get_OWM(zipcode):
    cloud_list = []
    sky_list = []
    user_token = '9738f6dd8889617a46ed1ab4109dffb6'
    full_api_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?zip=' + zipcode + ',us&cnt=16&units=imperial&APPID=' + user_token
    r = requests.get(full_api_url)
    weather_data = json.loads(r.text)
    weather_list = weather_data['list']
    for i in range(0,16):
        cloud_list.append(weather_list[i]['clouds'])
    return cloud_list

def displayWeather(cloud):
    today = now = datetime.datetime.now()
    date = today.day
    month = today.month
    print ('Weather Forecast: Cloudiness',)
    for i in range(0,16):
        print(month, (date+i), sep='/', end='' )
        print(': ', cloud[i], '%', '\t', sep= '', end='')
        if i == 7:
            print('\n')
def init_LED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

def control_LED(control):
    if control == 'on':
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18, GPIO.LOW)
    else:
        GPIO.output(24, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)


x = get_OWM('24060')
displayWeather(x)
playASound()
