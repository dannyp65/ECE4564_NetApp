import zipcode
from geopy.geocoders import Nominatim
myzip = zipcode.isequal('24061')

geolocator = Nominatim()
location = geolocator.geocode(myzip.city)
print((location.latitude, location.longitude))
print(location.address)
