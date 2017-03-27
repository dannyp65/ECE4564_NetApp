from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')

print(st.tle_latest(norad_cat_id=[25544, 41335], ordinal=1, format='tle'))
