import sys
import math
import ephem
import datetime
import calendar
from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')
import zipcode
from geopy.geocoders import Nominatim


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
    newevent = 0
    for p in range(45):
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
                    
            tr = ephem.Date(tr + 60.0 * ephem.second)
            if ending == False and washere == True:
                counter = counter + 1
            if counter == 5:
                print ("New Event!!!")
                masscounter = masscounter + 1
                ending = False
                washere = False
                counter = 0
                newevent = newevent + 1

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







