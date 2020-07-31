import numpy as np
from sklearn.cluster import AgglomerativeClustering
import geopy
from geopy.distance import geodesic
from scipy.cluster.hierarchy import fclusterdata
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from app import db
from app.models.model import User, GroupSize, Group


# from app.models.model import User, Preference, GroupSize
def match_routine():
    unpaired = User.query.filter(User.group_id == None)
    for size in [GroupSize.small, GroupSize.medium, GroupSize.large]:
        users = unpaired.filter(User.preferences.has(group_size=size)).all()
        print("Num Users for size", users)
        match(users, size)


def match(users, group_size):
    num_clusters = max(int(len(users)/2), 1)
    if group_size == GroupSize.medium:
        num_clusters = max(int(len(users)/4), 1)
    elif group_size == GroupSize.large:
        num_clusters = max(int(len(users)/8), 1)
    data = [user.get_preference_details_as_list() for user in users]
    if not data:
        return
    print(data)
    model = AgglomerativeClustering(n_clusters=num_clusters, affinity=sim_affinity, linkage='average')
    model.fit(data)
    labels = {}
    for i, v in enumerate(model.labels_):
        if v not in labels:
            labels[v] = []
        labels[v].append(users[i])
    
    for k, v in labels.items():
        g = Group()
        g.users = v
        db.session.add(g)
        db.session.commit()
        for user in users:
            user.send_paired_email(g)
        
    # case where is small


def sim(x, y):
    coordinatesX, coordinatesY = (x[0], x[1]), (y[0], y[1])
    group_sizeX = x[2]
    group_sizeY = y[2]
    school_levelX, schoolLevelY = x[3], y[3]
    hangout_outsideX, hangout_outsideY = x[4], y[4]
    position_typeX, position_typeY  = x[5], y[5]
    distance = geodesic(coordinatesX, coordinatesY).miles
    if distance < 50:
        score = 1
    elif distance < 100:
        score = 0.9
    elif distance < 1000:
        score = 0.7
    elif distance < 5000:
        score = 0.5
    else:
        score = 0
    
    locScore = score
    x = [group_sizeX, school_levelX, hangout_outsideX, position_typeX]
    y = [group_sizeY, schoolLevelY, hangout_outsideY, position_typeY]
    return 1.0 - np.sum(np.equal(np.array(x), np.array(y)))/len(x) - locScore

# Method to calculate distances between all sample pairs
from sklearn.metrics import pairwise_distances
def sim_affinity(X):
    return pairwise_distances(X, metric=sim)


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

    matrix = np.column_stack([model.children_])
    return matrix

# if __name__ == "__main__":
#     main()