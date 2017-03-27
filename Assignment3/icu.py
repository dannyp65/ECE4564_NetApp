import requests
import json
from twilio.rest import Client
import datetime
import pygame

now = datetime.datetime.now()

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
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(to=tonum, from_="+18045523194",
                                     body=mess)
    print(message)
    #return message

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


x = get_OWM('24060')
#print(x)
displayWeather(x)
playASound()
