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
    """
    now = datetime.datetime.utcnow()
    observer.date = now
    """
    for p in range(15):
        tr, azr, tt, altt, ts, azs = observer.next_pass(sat)

        while tr < ts:
            observer.date = tr
            sun = ephem.Sun()
            sun.compute(observer)
            sat.compute(observer)
            sun_alt = math.degrees(sun.alt)
            #print (sun_alt)
            if sat.eclipsed is False and -18 < sun_alt < -6:
                print ("%s %4.1f %5.1f" % (tr, math.degrees(sat.alt), math.degrees(sat.az)))
            tr = ephem.Date(tr + 60.0 * ephem.second)  

        
        observer.date = tr + ephem.minute

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

#iss = ephem.readtle(name, tle0, tle1)

"""
for p in range(3):
    tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
    while tr < ts :
        obs.date = tr
        iss.compute(obs)
        print ("%s %4.1f %5.1f" % (tr, math.degrees(iss.alt), math.degrees(iss.az)))
        tr = ephem.Date(tr + 60.0 * ephem.second)
    print
    obs.date = tr + ephem.minute
"""
#--------------------------------------------------------------------------
alt = 0
#print (get_next_pass(location.latitude, location.longitude, alt, name, tle0, tle1))

i = 0
while 1:
    get_next_pass(location.latitude, location.longitude, alt, name, tle0, tle1)
    print ("Satellite Information:")
    tleInfo = st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle')
    print (tleInfo)
    tle = ''.join(tleInfo)
    tle0, tle1 = tle.splitlines()
    








