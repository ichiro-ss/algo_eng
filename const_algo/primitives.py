import numpy as np

def read_points(f) -> dict:
    """Read the input file"""
    indexofpoint = {}
    for line in f:
        if line and 0x30 <= ord(line[0]) <=0x39:    # only 0-9
            i, x, y = (float(s) for s in line.split())
            indexofpoint[(x, y)] = int(i)-1
    return indexofpoint


def euclidean_distance(x, y):
    return np.sqrt(np.sum(np.square(x-y)))

def compute_distance_matrix(points):
    n = len(points)
    dists = np.array([[euclidean_distance(points[i], points[j]) for j in range(n)] for i in range(n)])

    return dists

def score(route, dists):
    # round distance value to integer
    dis = round(dists[route[-1]][route[0]])
    for i in range(len(route)):
        if i:
            dis += round(dists[route[i-1]][route[i]])
    return dis
