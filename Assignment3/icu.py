import requests
import json
from twilio.rest import TwilioRestClient
from playsound import playsound


def sendMess(mess, num):
    tonum = '+1' + num
    twilio_sid = "AC3fc819a1fe2f836b25e54e0ef47ba23d"
    twilio_token = "52a06091ff97cdc10f3af0f6790c9daf"
    client = TwilioRestClient(twilio_sid, twilio_token)
    message = client.messages.create(to=tonum, from_="+18045523194",
                                     body=mess)
    print(message)
    #return message

def get_OWM(zipcode):
    cloud_list = []
    sky_list = []
    user_token = '9738f6dd8889617a46ed1ab4109dffb6'
    full_api_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?zip=' + zipcode + ',us&cnt=16&units=imperial&APPID=' + user_token
    print(full_api_url)
    r = requests.get(full_api_url)
    weather_data = json.loads(r.text)
    weather_list = weather_data['list']
    for i in range(0,16):
        cloud_list.append(weather_list[i]['clouds'])
        sky_list.append(weather_list[i]['description'])
    return cloud_list, sky_list



x, y = get_OWM('24060')
#print(x)
print(y[1])
#print(y[1][1])
print(type(y[1]))
newlist = []
for i in range(0,16):
    newlist.append(y[i]['description'])
print(newlist)
#sendMess('Hello Again Daniel!', '4342497554')
playsound('/Users/danielpham/Downloads/sms.mp3')