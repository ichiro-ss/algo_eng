import sys
import math
from primitives import *
import numpy as np
import time
sys.setrecursionlimit(10**9)

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

def solve_tsp_2approx(points, dists):
    # Step 1: Compute the Euclidean distance between eah pair of cities
    n = len(points)

    # Step 2: Compute the minimum spanning tree of the complete graph
    # Step 3: duplicate the branches of the minimum spanning tree and create an Eulerian graph
    mst = kruskal(dists)


    # Step 4: Convert the preorder traversal into a Hamiltonian cycle by skipping duplicate vertices
    tour = []
    to_cycle(-1, 0, n, mst, tour)
    return tour

def main(instance):
    with open("instances/"+instance+".tsp") as inputfile:
        try:
            indexofpoint = read_points(inputfile)
        except FileNotFoundError as err:
            print(err)

    points = np.array(list(indexofpoint.keys()))
    distance_matrix = compute_distance_matrix(points)

    st = time.perf_counter()
    cycle = solve_tsp_2approx(points, distance_matrix)
    en = time.perf_counter()

    return cycle, score(cycle, distance_matrix), en-st

if __name__ == "__main__":
    # input
    basename, extname = sys.argv[-1].split(".")
    if extname == "tsp":
        ans, score = main(basename)
        print(basename, ans)
        print("score", score)
    elif extname == "txt":
        with open("instances/"+basename+".txt") as inputfile:
            try:
                for line in inputfile.read().splitlines():
                    ans, score = main(line)
                    print(line, ans)
                    print("score:", score)
            except FileNotFoundError as err:
                print(err)
