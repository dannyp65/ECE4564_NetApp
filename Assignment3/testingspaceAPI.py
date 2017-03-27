from spacetrack import SpaceTrackClient
st = SpaceTrackClient('jstrad@vt.edu', 'johnnyboy1234567')

#print(st.tle_latest(norad_cat_id=[25544, 41335], ordinal=1, format='tle'))

output = st.tle_latest(ordinal=1, epoch='>now-30',
              mean_motion=op.inclusive_range(0.99, 1.01),
              eccentricity=op.less_than(0.01), format='tle')
print (output)
