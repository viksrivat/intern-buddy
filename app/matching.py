import numpy as np
from app.models import model
from sklearn.cluster import AgglomerativeClustering
import geopy
from geopy.distance import geodesic
from scipy.cluster.hierarchy import fclusterdata
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

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
    return score


def getChildrenDistPair(model):
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    matrix = np.column_stack([model.children_, model.distances_])
    print(matrix)
    return matrix


# data = np.array([[1,0,2],[2,3,4],[1,5,1],[3,4,5],[1,0,9]])
data = np.random.randn(5,3)

# setting distance_threshold=0 ensures we compute the full tree.
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
model.fit(data)
getChildrenDistPair(model)

