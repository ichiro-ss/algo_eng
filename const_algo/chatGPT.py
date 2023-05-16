import math
import sys
import numpy as np
import random
from primitives import *
import time

# def euclidean_distance(p1, p2):
#     return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def tsp_2approx(coords):
    # Step 1: Compute the Euclidean distance between each pair of cities
    n = len(coords)
    dist = [[euclidean_distance(coords[i], coords[j]) for j in range(n)] for i in range(n)]

    # Step 2: Compute the minimum spanning tree of the complete graph
    visited = [False] * n
    parent = [None] * n
    key = [float('inf')] * n
    key[0] = 0
    for i in range(n):
        u = min((key[j], j) for j in range(n) if not visited[j])[1]
        visited[u] = True
        for v in range(n):
            if not visited[v] and dist[u][v] < key[v]:
                key[v] = dist[u][v]
                parent[v] = u

    # Step 3: Perform a depth-first search of the minimum spanning tree to obtain a preorder traversal
    preorder = []
    stack = [0]
    while stack:
        u = stack.pop()
        preorder.append(u)
        for v in range(n):
            if parent[v] == u:
                stack.append(v)

    # Step 4: Convert the preorder traversal into a Hamiltonian cycle by skipping duplicate vertices
    visited = [False] * n
    cycle = []
    for u in preorder:
        if not visited[u]:
            visited[u] = True
            cycle.append(u)

    return cycle

def main(instance):
    with open("instances/"+instance+".tsp") as inputfile:
        try:
            indexofpoint = read_points(inputfile)
        except FileNotFoundError as err:
            print(err)

    points = np.array(list(indexofpoint.keys()))
    distance_matrix = compute_distance_matrix(points)

    st = time.perf_counter()
    # Solve the TSP using the 2-approximation algorithm
    cycle = tsp_2approx(points)
    en = time.perf_counter()

    return points, cycle, score(cycle, distance_matrix), en-st

if __name__ == "__main__":
    # input
    basename, extname = sys.argv[-1].split(".")
    if extname == "tsp":
        ans, score = main(basename)
        print(basename, ans)
        print("score:", score)
    elif extname == "txt":
        with open("instances/"+basename+".txt") as inputfile:
            try:
                for line in inputfile.read().splitlines():
                    ans, score = main(line)
                    print(line, ans)
                    print("score:", score)
            except FileNotFoundError as err:
                print(err)


