<<<<<<< HEAD
import sys
import math
import ephem
import datetime
import time
import calendar
from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')
import zipcode
from geopy.geocoders import Nominatim
import requests
import json
from twilio.rest import TwilioRestClient
import pygame
import RPi.GPIO as GPIO

dates_viewable = []

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

def seconds_between(d1, d2):
    return abs((d2 - d1).seconds)

def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt

def displayWeather(cloud):
    today = datetime.date.today()
    date = today.day
    month = today.month
    try:
        if len(cloud) == 16:
            print ('Weather Forecast: Cloudiness',)
            for i in range(0,16):
                print(today.month, today.day, sep='/', end='' )
                print(': ', cloud[i], '%', '\t', sep= '', end='')
                if i == 7:
                    print('\n')
                today += datetime.timedelta(days=1)
            print("")
    except Exception as a:
        print('Error: Cannot display weather data!')

def get_OWM(zipcode):
    cloud_list = []
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

def get_next_pass(lat, lon, alt, name, tle0, tle1, zipcode):
    sat = ephem.readtle(name, tle0, tle1)
    today = datetime.date.today()
    different_day = today - today
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.long = str(lon)
    observer.elevation = alt
    observer.pressure = 0
    observer.horizon = '-0:34'
    counter = 0
    ending = False
    washere = False
    time_flag = False
    weather_list = get_OWM(zipcode)
    displayWeather(weather_list)
    while different_day.days < 15:
        ending = False
        tr, azr, tt, altt, ts, azs = observer.next_pass(sat)
        while tr < ts:
            ending = False
            observer.date = tr
            sun = ephem.Sun()
            sun.compute(observer)
            sat.compute(observer)
            sun_alt = math.degrees(sun.alt)

            year2, month2, day2, hour2, minute2, second2 = tr.tuple()
            visible_day = datetime.date(year2, month2, day2)
            different_day = visible_day - today
            if sat.eclipsed is False and -18 < sun_alt < -6 and weather_list[different_day.days] < 21:
                print ("%s %4.1f %5.1f %4.1f %+6.1f" % (tr, math.degrees(sat.alt), math.degrees(sat.az), math.degrees(sat.sublat), math.degrees(sat.sublong)))
                ending = True
                washere = True
                if time_flag == False:
                    time_flag = True
                    year, month, day, hour, minute, second = tr.tuple()
                    dates_viewable.append(datetime.datetime(year, month, day, hour, minute, int(second)))
            tr = ephem.Date(tr + 60.0 * ephem.second)
            if ending == False and washere == True:
                counter = counter + 1
                print ("New Event")
                ending = False
                washere = False
                time_flag = False
        if counter == 5:
            print ("Five Events Reached!")
            ending = False
            washere = False
            counter = 0
            break
        observer.date = tr + ephem.minute
    print("There are " + str(counter) + "viewable events in the next 15 days")
    print("---------------------------------------------------------")
           

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
    mess1 = "Next viewable event: " + mess
    message = client.messages.create(to=tonum, from_="+18045523194",
                                     body=mess1)


#---------------------------------------------------------------------
zip, sat = get_args()

init_LED()

myzip = zipcode.isequal(zip)
geolocator = Nominatim()
location = geolocator.geocode(myzip.city)

print ("Satellite Information:")
tleInfo = st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle')

tle = ''.join(tleInfo)
tle0, tle1 = tle.splitlines()


print(st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle'))
print ("Zip Information:")
print((location.latitude, location.longitude))
#print(location.address)

#print (tle0)
#print ("---------------------------------")
#print (tle1)
#print ("---------------------------------")

name = "ISS (ZARYA)"
#--------------------------------------------------------------------------
alt = 0
get_next_pass(location.latitude, location.longitude, alt, name, tle0, tle1, zip)
num_day = len(dates_viewable)
led = False
text = False
sound = False
currstate = 0
while 1:
    today = dates_viewable[0]
    if currstate == 0:
        for i in range(0, num_day):
            diff_day = dates_viewable[i]- today
            if diff_day.days == 0 and diff_day.seconds < (15*60):
                currstate = 1
                text = True
    elif currstate == 1:
        if diff_day.days == 0 and diff_day.seconds > (15*60):
            currstate = 0
        if text:
            sendMess(str(dates_viewable[0]), "4342497554")
            text = False
        control_LED('off')
        time.sleep(1)
        control_LED('on')
        playASound()






=======
import sys
import math
import ephem
import datetime
import calendar
from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')
import zipcode
from geopy.geocoders import Nominatim

dates_viewable = []

def seconds_between(d1, d2):
    return abs((d2 - d1).seconds)

def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt

def get_next_pass(lat, lon, alt, name, tle0, tle1):
    sat = ephem.readtle(name, tle0, tle1)

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.long = str(lon)
    observer.elevation = alt
    observer.pressure = 0
    observer.horizon = '-0:34'
    counter = 0
    masscounter = 0
    ending = False
    washere = False
    time_flag = False
    for p in range(500):
        ending = False
        tr, azr, tt, altt, ts, azs = observer.next_pass(sat)
        while tr < ts:
            ending = False
            observer.date = tr
            sun = ephem.Sun()
            sun.compute(observer)
            sat.compute(observer)
            sun_alt = math.degrees(sun.alt)
            if sat.eclipsed is False and -18 < sun_alt < -6:
                print ("%s %4.1f %5.1f %4.1f %+6.1f" % (tr, math.degrees(sat.alt), math.degrees(sat.az), math.degrees(sat.sublat), math.degrees(sat.sublong)))
                ending = True
                washere = True
                if time_flag == False:
                    time_flag = True
                    year1, month1, day1, hour, minute, second = tr.tuple()
                    
            tr = ephem.Date(tr + 60.0 * ephem.second)
            if ending == False and washere == True:
                year, month, day, hour1, minute1, second1 = tr.tuple()
                dates_viewable.append(datetime.datetime(year, month, day, hour, minute, int(second)))
                counter = counter + 1
                print ("New Event")
                ending = False
                washere = False
                time_flag = False
            if counter == 5:
                print ("Five Events Reached!")
                masscounter = masscounter + 1
                ending = False
                washere = False
                counter = 0
                print(dates_viewable)
                break
   
        observer.date = tr + ephem.minute
    print("---------------------------------------------------------")
           

#---------------------------------------------------------------------

myzip = zipcode.isequal('24061')
geolocator = Nominatim()
location = geolocator.geocode(myzip.city)

print ("Satellite Information:")
tleInfo = st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle')

tle = ''.join(tleInfo)
tle0, tle1 = tle.splitlines()


print(st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle'))
print ("Zip Information:")
print((location.latitude, location.longitude))
print(location.address)

print (tle0)
print ("---------------------------------")
print (tle1)
print ("---------------------------------")

name = "ISS (ZARYA)"

readonce = True
#--------------------------------------------------------------------------
alt = 0
programrunning = True
while programrunning:
    get_next_pass(location.latitude, location.longitude, alt, name, tle0, tle1)







>>>>>>> f8edb0e8d02fd2be11e13690565e05f8db090c75
