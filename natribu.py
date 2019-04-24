import random
from geographiclib.geodesic import Geodesic
from collections import namedtuple
from bisect import bisect

def geowrapper():
    GeoPoint = namedtuple('GeoPoint', ['lat','lon'])

    compass = [
        'N'  ,
        'NNE',
        'NE' ,
        'ENE',
        'E'  ,
        'ESE',
        'SE' ,
        'SSE',
        'S'  ,
        'SSW',
        'SW' ,
        'WSW',
        'W'  ,
        'WNW',
        'NW' ,
        'NNW',
        'N'  ,
    ]

    degrees = [
          0  ,
         22.5,
         45  ,
         67.5,
         90  ,
        112.5,
        135  ,
        157.5,
        180  ,
        202.5,
        225  ,
        247.5,
        270  ,
        292.5,
        315  ,
        337.5,
        360  ,
    ]

    def randpoint():
        lat = random.random() * 90.0
        lon = random.random() * 180.0
        if random.randint(0, 1) == 1:
            lat = -lat
        if random.randint(0, 1) == 1:
            lon = -lon
        return GeoPoint(lat, lon)

    def randazimuth(c):
        c = GeoPoint(*c) #compatibility with ordinary tuples
        geod = Geodesic.WGS84
        res = {'s12' : 0}
        p = randpoint()
        while res['s12'] < 500000:
            res = geod.Inverse(c.lat, c.lon, p.lat, p.lon)
        a = res['azi1']
        if a < 0:
            a += 360
        i = bisect(degrees, a)
        if a - degrees[i - 1] < 11.25:
            i -= 1
        return p, a, compass[i]

    return randazimuth
