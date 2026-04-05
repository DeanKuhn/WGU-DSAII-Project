from sklearn.manifold import MDS
from sklearn.cluster import KMeans

import numpy as np

def build_address_index_map(locations_matrix):
    # build a dictionary mapping addres strings to their location ID
    # allows fast lookups instead of searching the list every time

    address_map = {}
    for row in locations_matrix:
        address = row[1]
        location_id = row[0]
        address_map[address] = location_id
    return address_map

def build_sub_matrix(packages, distances_matrix, locations_matrix):
    # this function actually takes into account the fact that there may be
    # distances on the distance_matrix loaded from the csv that no packages are
    # assigned to, so it will skip them when creating the 2D matrix

    # get the address from each package
    # this only gets the addresses we will actually need
    address_map = build_address_index_map(locations_matrix)
    indices = []
    for p in packages:
        # find location_id of package by finding it in the address map based
        # off the address member of the package object
        location_id = address_map[p.address]
        indices.append(location_id)

    # create sub matrix

    sub_matrix = []
    for i in indices:
        row = []
        for j in indices:
            distance = distances_matrix[i][j]
            row.append(distance)
        sub_matrix.append(row)

    return np.array(sub_matrix), indices

def get_coords_from_matrix(sub_matrix):
    # MDS taks a matrix of pairwise distances and tris to find 2D coordinates
    # that preserve those distances as closely as possible
    # we do this because KMeans needs (x, y) coordinates to work
    # initiate mds
    mds = MDS(n_components=2, metric='precomputed', random_state=42)

    coords = mds.fit_transform(sub_matrix)
    return coords

def cluster_packages(packages, distance_matrix, locations_matrix, k):
    sub_matrix, indices = build_sub_matrix(packages, distance_matrix, locations_matrix)
    coords = get_coords_from_matrix(sub_matrix)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(coords)

    # build and return the mapping from package_id to cluser label
    # use dict comprehension - enumerate(packages) gives us (i, package)
    # pairs, and labels[i] is the cluser index for that package
    # this dict is what gets passed into the GA fitness function later

    cluster_map = {}
    for i, p in enumerate(packages):
        cluster_map[p.package_id] = labels[i]
    return cluster_map