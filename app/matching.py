import numpy as np
from app.models import model
from sklearn.cluster import AgglomerativeClustering
import geopy
from geopy.distance import geodesic


def calculateLocationScore(location1, location2):
    # set 2700 miles
    # distance between Miami and Seattle is 2733.497
    max = 2700
    geolocator = geopy.Nominatim(user_agent="intern-buddy")
    geoLocation1 = geolocator.geocode(location1)
    coordinate1 = (geoLocation1.latitude, geoLocation1.longitude)
    geoLocation2 = geolocator.geocode(location2)
    coordinate2 = (geoLocation2.latitude, geoLocation2.longitude)
    distance = geodesic(coordinate1, coordinate2).miles

    if distance > max:
        score = 0
    else:
        score = round((1 - distance/max), 1)
    print(distance, score)
    return score

