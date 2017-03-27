import sys
import math
import ephem

iss = ephem.readtle("ISS (ZARYA)",
  "1 25544U 98067A   17084.90100100 +.00002847 +00000-0 +50029-4 0  9992",
  "2 25544 051.6418 093.4538 0007279 338.2943 091.9717 15.54260139048806")

obs = ephem.Observer()
obs.lat = '37.2296566'
obs.long = '-80.4136766'

for p in range(3):
    tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
    while tr < ts :
        obs.date = tr
        iss.compute(obs)
        print ("%s %4.1f %5.1f" % (tr, math.degrees(iss.alt), math.degrees(iss.az)))
        tr = ephem.Date(tr + 60.0 * ephem.second)
    print
    obs.date = tr + ephem.minute
