#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# ==============================================================================
# aviationFormula - Some useful formula in globe and aviation context
# Copyright (C) 2018  Oliver Clemens
# 
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <https://www.gnu.org/licenses/>.
# ==============================================================================
# Inspired by Aviation Formulary V1.46 by Ed Williams.
# -> http://www.edwilliams.org/avform.htm
# And the methods at Movable Type Scripts
# -> https://www.movable-type.co.uk/scripts/latlong.html
# ==============================================================================

from __future__ import division  # (at top of module)
from math import acos, asin, atan2, cos, degrees, pi, radians, sin, sqrt, tan
import unittest


# Calculates the great circle distance in arc angle (in radians).
def gc_distance_rad(lat_deg1, lon_deg1, lat_deg2, lon_deg2):
    # Haversine formula https://www.movable-type.co.uk/scripts/latlong.html
    lat1 = radians(lat_deg1)
    lat2 = radians(lat_deg2)
    dlat = radians(lat_deg2 - lat_deg1)
    dlon = radians(lon_deg2 - lon_deg1)
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * atan2(sqrt(a), sqrt(1 - a))


# Calculates the great circle distance in nautical miles.
def gc_distance_nm(lat_deg1, lon_deg1, lat_deg2, lon_deg2):
    radius_earth_m = 6371008.7714  # Mean radius earth WGS-84
    radius_earth_nm = radius_earth_m / 1852
    return gc_distance_rad(lat_deg1, lon_deg1, lat_deg2, lon_deg2) * radius_earth_nm


# Calculates the initial bearing in degrees
def init_bearing_deg(lat_deg1, lon_deg1, lat_deg2, lon_deg2):
    lat1 = radians(lat_deg1)
    lat2 = radians(lat_deg2)
    dlon = radians(lon_deg2 - lon_deg1)
    return normalize_angle_deg(degrees(atan2(sin(dlon) * cos(lat2),
                         cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon))))


# Calculate the final bearing in degrees
def final_bearing_deg(lat_deg1, lon_deg1, lat_deg2, lon_deg2):
    return normalize_angle_deg(init_bearing_deg(lat_deg2, lon_deg2, lat_deg1, lon_deg1) + 180)


# Normalise to compass bearing (0 to 360 degrees)
def normalize_angle_deg(angle_deg):
    return angle_deg % 360.0


# Normalise to -180 to +180 degrees
def normalize_longitude_deg(lon_deg):
    return (lon_deg + 540.0) % 360.0 - 180.0


# Calculates the intermediate coordinates of two points.
# The optional 5th argument is the relative distance to point 1.
# 0 returns point 1, 1 returns point 2. Default is 0.5 and the middle.
def gc_intermediate_point(lat_deg1, lon_deg1, lat_deg2, lon_deg2, fraction=0.5):
    lat1 = radians(lat_deg1)
    lat2 = radians(lat_deg2)
    lon1 = radians(lon_deg1)
    lon2 = radians(lon_deg2)

    fraction = min(max(fraction, 0.0), 1.0)

    # Calc gc distance in rad between points.
    d = gc_distance_rad(lat_deg1, lon_deg1, lat_deg2, lon_deg2)

    # Calc intermediate point.
    if d:
        a = sin((1-fraction) * d) / sin(d)
        b = sin(fraction * d) / sin(d)
        x = a * cos(lat1) * cos(lon1) + b * cos(lat2) * cos(lon2)
        y = a * cos(lat1) * sin(lon1) + b * cos(lat2) * sin(lon2)
        z = a * sin(lat1) + b * sin(lat2)
        lat = atan2(z, sqrt(x ** 2 + y ** 2))
        lon = atan2(y, x)
        return (degrees(lat),degrees(lon))
    else:
        return (lat_deg1, lon_deg1)


def point_at_distance_and_bearing(lat_deg1, lon_deg1, distance_nm, init_bearing_deg):
    lat1 = radians(lat_deg1)
    lon1 = radians(lon_deg1)
    radius_earth_m = 6371008.7714  # Mean radius earth WGS-84
    radius_earth_nm = radius_earth_m / 1852
    distance_rad = distance_nm / radius_earth_nm
    init_bearing = init_bearing_deg / 180 * pi
    lat2 = asin(sin(lat1) * cos(distance_rad) + cos(lat1) * sin(distance_rad) * cos(init_bearing))
    lon2 = lon1 + atan2(sin(init_bearing) * sin(distance_rad) * cos(lat1),
                        cos(distance_rad) - sin(lat1) * sin(lat2))
    return (degrees(lat2), normalize_longitude_deg(degrees(lon2)))


def cross_track_distance_rad(lat_deg1, lon_deg1, lat_deg2, lon_deg2, lat_deg3, lon_deg3):
    distance_13_rad = gc_distance_rad(lat_deg1, lon_deg1, lat_deg3, lon_deg3)
    bearing_13_rad = radians(init_bearing_deg(lat_deg1, lon_deg1, lat_deg3, lon_deg3))
    bearing_12_rad = radians(init_bearing_deg(lat_deg1, lon_deg1, lat_deg2, lon_deg2))
    return asin(sin(distance_13_rad) * sin(bearing_13_rad - bearing_12_rad))

class AviationFormula(unittest.TestCase):
    def test_gc_distance_rad(self):
        lat1_deg = 50
        lon1_deg = 10
        lat2_deg = -10
        lon2_deg = -30
        self.assertAlmostEqual(gc_distance_nm(lat1_deg, lon1_deg, lat2_deg, lon2_deg), 4166.596, places=1)

    def test_init_bearing_deg(self):
        lat1_deg = 50
        lon1_deg = 10
        lat2_deg = -10
        lon2_deg = -30
        self.assertAlmostEqual(init_bearing_deg(lat1_deg, lon1_deg, lat2_deg, lon2_deg), 222.554, places=1)

    def test_final_bearing_deg(self):
        lat1_deg = 50
        lon1_deg = 10
        lat2_deg = -10
        lon2_deg = -30
        self.assertAlmostEqual(final_bearing_deg(lat1_deg, lon1_deg, lat2_deg, lon2_deg), 206.194, places=1)

    def test_normalized_angle_deg(self):
        angle_deg = -137.446
        self.assertAlmostEqual(normalize_angle_deg(angle_deg), 222.554, places=1)

    def test_normalize_lon_deg(self):
        angle_deg = -137.446
        self.assertAlmostEqual(normalize_longitude_deg(angle_deg), -137.446, places=1)

    def test_gc_intermediate_point(self):
        lat1_deg = 50
        lon1_deg = 10
        lat2_deg = -10
        lon2_deg = -30
        lat3, lon3 = gc_intermediate_point(lat1_deg, lon1_deg, lat2_deg, lon2_deg)
        self.assertAlmostEqual(lat3, 21.117, places=1)
        self.assertAlmostEqual(lon3, -14.374, places=1)

    def test_point_at_distance_and_bearing(self):
        lat1_deg = -10.0
        lon1_deg = -30.0
        bearing_deg = 200.0
        distance_nm = 1000.0
        lat2, lon2 = point_at_distance_and_bearing(lat1_deg, lon1_deg, distance_nm, bearing_deg)
        self.assertAlmostEqual(lat2, -25.599, places=1)
        self.assertAlmostEqual(lon2, -36.239, places=1)

    def test_cross_track_distance_rad(self):
        # Example from Ed Williams
        lat1_deg = 33.0 + 57/60.0
        lon1_deg = -118 - 24/60.0
        lat2_deg = 40.0 + 38/60.0
        lon2_deg = -73.0 - 47/60.0
        lat3_deg = 34.5
        lon3_deg = -116.5
        self.assertAlmostEqual(cross_track_distance_rad(lat1_deg, lon1_deg, lat2_deg, lon2_deg, lat3_deg, lon3_deg),
                               0.00216778, places=5)


if __name__ == '__main__':
    unittest.main()