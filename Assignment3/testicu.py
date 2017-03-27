import sys
import math
import ephem
from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')
import zipcode
from geopy.geocoders import Nominatim

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

iss = ephem.readtle("ISS (ZARYA)", tle0, tle1)

obs = ephem.Observer()
obs.lat = location.latitude
obs.long = location.longitude

for p in range(3):
    tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
    while tr < ts :
        obs.date = tr
        iss.compute(obs)
        print ("%s %4.1f %5.1f" % (tr, math.degrees(iss.alt), math.degrees(iss.az)))
        tr = ephem.Date(tr + 60.0 * ephem.second)
    print
    obs.date = tr + ephem.minute

