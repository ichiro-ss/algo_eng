import sys
import math
from const_algo.primitives import *
import numpy as np

class UnionFind:
    def __init__(self, n):
        self.par = [-1] * n
        self.rank = [0] * n
    def root(self, x):
        if self.par[x] < 0:
            return x
        else:
            self.par[x] = self.root(self.par[x])
            return self.par[x]
    def unite(self, x, y):
        x, y = self.root(x), self.root(y)
        if x == y:
            return
        if self.rank[x] < self.rank[y]:
            self.par[x] = y
        else:
            self.par[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1
    def are_same(self, x, y):
        return self.root(x) == self.root(y)

def eval_tsp(route, distance_matrix):
    dis = distance_matrix[route[-1]][route[0]]
    for i in range(len(route)):
        if i:
            dis += distance_matrix[route[i-1]][route[i]]
    return dis

def euclidean_distance(x, y):
    return np.sqrt(np.sum(np.square(x-y)))

def compute_distance_matrix(points):
    n = len(points)
    distance_matrix = np.array([[euclidean_distance(points[i], points[j]) for j in range(n)] for i in range(n)])

    return distance_matrix

# return minimum spanning tree ~~~mst: linked list
def kruskal(distance_matrix) -> list:
    n = len(distance_matrix)
    Edges = []
    for i in range(n):
        for j in range(i+1, n):
            Edges.append((distance_matrix[i, j], (i, j)))
    Edges.sort()
    uf = UnionFind(n)
    mst = [[] for _ in range(n)]
    for _, (u, v) in Edges:
        if uf.are_same(u, v):
            continue
        else:
            mst[u].append(v)
            mst[v].append(u)
            uf.unite(u, v)

    return mst

def to_cycle(pre, now, n, mst, tour):
    tour.append(now)
    for next in mst[now]:
        if next == pre:
            continue
        to_cycle(now, next, n, mst, tour)

def solve_tsp_2approx(points):
    # Step 1: Compute the Euclidean distance between eah pair of cities
    n = len(points)
    distance_matrix = compute_distance_matrix(points)

    # Step 2: Compute the minimum spanning tree of the complete graph
    # Step 3: duplicate the branches of the minimum spanning tree and create an Eulerian graph
    mst = kruskal(distance_matrix)


    # Step 4: Convert the preorder traversal into a Hamiltonian cycle by skipping duplicate vertices
    tour = []
    to_cycle(-1, 0, n, mst, tour)
    return tour

# input
basename = sys.argv[-1].split(".")[0]

with open(basename+".tsp") as inputfile:
    try:
        indexofpoint = read_points(inputfile)
    except FileNotFoundError as err:
        print(err)

points = np.array(list(indexofpoint.keys()))

# compute distance matrix

tour = solve_tsp_2approx(points)
print("ans:", tour)
print("score:", eval_tsp(tour, compute_distance_matrix(points)))
