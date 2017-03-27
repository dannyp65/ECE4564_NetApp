from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')
import zipcode
from geopy.geocoders import Nominatim

myzip = zipcode.isequal('24061')
geolocator = Nominatim()
location = geolocator.geocode(myzip.city)

print ("Satellite Information:")
print(st.tle_latest(norad_cat_id=[25544], ordinal=1, format='tle'))
print ("Zip Information:")
print((location.latitude, location.longitude))
print(location.address)
