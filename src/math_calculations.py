import numpy as np
from scipy.signal import argrelextrema


def haversine_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    Updated "math" library to "numpy". Due to dataframe calculation problems.
    Haversine distance between two points, expressed in meters.
    Implemented from http://www.movable-type.co.uk/scripts/latlong.html
    """
    EARTH_RADIUS = 6378.137 * 1000
    d_lon = np.radians(longitude_1 - longitude_2)
    lat1 = np.radians(latitude_1)
    lat2 = np.radians(latitude_2)
    d_lat = lat1 - lat2

    a = np.power(np.sin(d_lat/2), 2) + \
        np.power(np.sin(d_lon/2), 2) * np.cos(lat1) * np.cos(lat2)
    c = 2 * np.arcsin(np.sqrt(a))
    d = EARTH_RADIUS * c

    return d


def elevation_angle(ele1, ele2, distance):
    return np.arctan((ele2-ele1)/distance)
