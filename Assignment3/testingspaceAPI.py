from spacetrack import SpaceTrackClient
import json
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')

allInfo = st.tle_latest(norad_cat_id=[25544], ordinal=1, format = "name")
strInfo = ''.join(allInfo)
splitStr = strInfo.split(',')
namepos = splitStr.index('"OBJECT_NAME":"ISS (ZARYA)"')
object = splitStr[namepos]
object1, name = object.split(':')
print(name)

tleInfo = st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle')

tle = ''.join(tleInfo)
tle0, tle1 = tle.splitlines()
print(tle0)
print(tle1)



 
