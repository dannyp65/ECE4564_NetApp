#/usr/bin/env python3
import requests
import json
from twilio.rest import TwilioRestClient
import datetime
import sys
import pygame
#import RPi.GPIO as GPIO

now = datetime.datetime.now()
def get_args():
    opt_in_opt = "ERROR: cannot take another opt flag as a parameter"
    cmd_args = sys.argv
    zip_op = '-z'
    sat_op = '-s'
    if len(cmd_args) != 5:
        print('Error: Invalid number of argument!')
        sys.exit()  # raise SystemExit
    cmd_len = len(cmd_args)
    if cmd_args[1] == zip_op and cmd_args[3] == sat_op:
        zip = cmd_args[2]
        sat = cmd_args[4]
        if len(zip) != 5:
            print('Error: Invalid Zipcode!')
            sys.exit()
    else:
        print('Error: Invalid parameters')
        sys.exit()
    return zip, sat


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
    if len(zipcode) != 5:
        print('Error: Invalid zipcode in get_OWM(zipcode) call!')
        sys.exit()
    try:
        r = requests.get(full_api_url)
    except:
        print('Error: Weather API request error!')
        sys.exit()
    try:
        weather_data = json.loads(r.text)
        weather_list = weather_data['list']
        for i in range(0,16):
            cloud_list.append(weather_list[i]['clouds'])
        return cloud_list
    except:
        print('Error: Invalid response from weather API')
        sys.exit()

def displayWeather(cloud):
    today = now = datetime.datetime.now()
    date = today.day
    month = today.month
    try:
        if len(cloud) == 16:
            print ('Weather Forecast: Cloudiness',)
            for i in range(0,16):
                print(month, (date+i), sep='/', end='' )
                print(': ', cloud[i], '%', '\t', sep= '', end='')
                if i == 7:
                    print('\n')
    except Exception as a:
        print('Error: Cannot display weather data!')

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




zip, sat = get_args()
x = get_OWM('24060')

displayWeather(get_OWM(zip))
playASound()
print(zip,sat)