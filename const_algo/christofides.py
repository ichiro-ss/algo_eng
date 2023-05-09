import sys
import math
from const_algo.primitives import *
import numpy as np
sys.setrecursionlimit(10 ** 9)
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

# evaluate tsp solution
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

# return minimum spanning tree ~~~mst: (u, v, weight)
def kruskal(distance_matrix) -> list:
    n = len(distance_matrix)
    Edges = []
    for i in range(n):
        for j in range(i+1, n):
            Edges.append(distance_matrix[i, j], (i, j))

    uf = UnionFind(n)
    mst = []
    for weight, (u, v) in Edges:
        if uf.are_same(u, v):
            continue
        else:
            mst.append((u, v, weight))
            uf.unite(u, v)

    return mst

def find_odd_vertices(mst):
    degree = [0] * len(mst)
    for u, v, _ in mst:
        degree[u] += 1
        degree[v] += 1
    odd_vertices = [u for u in range(len(mst)) if degree[u] % 2]
    return odd_vertices

# Find the minimum weight perfect matching using the Hungarian algorithm
def min_weight_matching(odd_vertices, distance_matrix):
    # Construct a complete graph from the odd vertices
    # should write blossom algorithm or use networkx
    return

def eulerian_circuit(multigraph, start):
    # Find an Eulerian circuit in the multigraph using Hierholzer's algorithm
    # Note: This implementation has a time complexity of O(|E|)
    circuit = []
    stack = [start]
    while stack:
        u = stack[-1]
        if multigraph[u]:
            v, w = multigraph[u].pop()
            multigraph[v].remove((u, w))
            stack.append(v)
        else:
            circuit.append(stack.pop())
    circuit.reverse()
    return circuit

def christofides(points):
    # Step 1: Compute the minimum spanning tree of the complete graph of the cities
    n = len(points)
    distance_matrix = compute_distance_matrix(points)
    mst = kruskal(distance_matrix)

    # Step 2: Find the set of vertices with odd degree in the MST and construct a minimum-weight perfect matching between them
    odd_vertices = find_odd_vertices(mst)

    # Step 4: Find a minimum-weight perfect matching between the odd-degree vertices
    matching = min_weight_matching(odd_vertices, distance_matrix)

    # Step 5: Combine the edges of the MST and the matching to form a multigraph
    multigraph = mst + [(odd_vertices[i], odd_vertices[j]) for i,j in matching]
    circuit = []
    visited = np.zeros(len(multigraph), dtype=bool)
    i = 0
    while len(circuit) < len(multigraph):
        circuit.append(multigraph[i])
        visited[i] = True
        i = np.argwhere(multigraph[i][1] == np.array([e[0] for e in multigraph if not visited[e[0]]]))[0][0]
    tour = []
    # for edge in
    # Shortcutting to obtain a Hamiltonian tour
    visited = np.zeros(n, dtype=bool)
    current_node = circuit[0][0]
    visited[current_node] = True
    tour = [current_node]
    while len(tour) < n:
        for edge in circuit:
            if edge[0] == current_node and not visited[edge[1]]:
                tour.append(edge[1])
                visited[edge[1]] = True
                current_node = edge[1]
                break
            elif edge[1] == current_node and not visited[edge[0]]:
                tour.append(edge[0])
                visited[edge[0]] = True
                current_node = edge[0]
                break
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

tour = christofides(points)
