import heapq
import math
import sys
from const_algo.primitives import read_points
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def minimum_spanning_tree(graph):
    n = len(graph)
    visited = [False] * n
    heap = [(0, 0)] # (weight, vertex)
    mst = []
    while heap:
        w, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        mst.append((u, w))
        for v, weight in graph[u]:
            if not visited[v]:
                heapq.heappush(heap, (weight, v))
    return mst

def find_odd_vertices(mst):
    degree = [0] * len(mst)
    for u, v in mst:
        degree[u] += 1
        degree[v] += 1
    odd_vertices = [u for u in range(len(mst)) if degree[u] % 2 == 1]
    return odd_vertices

def minimum_weight_matching(graph, odd_vertices):
    n = len(graph)
    matching = []
    visited = [False] * n
    for u in odd_vertices:
        visited[u] = True
        for v, w in graph[u]:
            if not visited[v] and v in odd_vertices:
                matching.append((u, v, w))
                visited[v] = True
                break
    return matching

def eulerian_circuit(graph, start):
    n = len(graph)
    circuit = []
    stack = [start]
    while stack:
        u = stack[-1]
        if graph[u]:
            v, w = graph[u].pop()
            graph[v] = [(u, w2) for u, w2 in graph[v] if u != u]
            stack.append(v)
        else:
            circuit.append(stack.pop())
    return circuit[::-1]

def christofides_tsp(coords):
    n = len(coords)

    # Step 1: Compute the complete graph with edge weights as Euclidean distances
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            weight = euclidean_distance(coords[i], coords[j])
            graph[i].append((j, weight))
            graph[j].append((i, weight))

    # Step 2: Compute the minimum spanning tree of the graph
    mst = minimum_spanning_tree(graph)

    # Step 3: Find the set of vertices with odd degree in the MST
    odd_vertices = find_odd_vertices(mst)

    # Step 4: Find a minimum-weight perfect matching between the odd-degree vertices
    matching = minimum_weight_matching(graph, odd_vertices)

    # Step 5: Combine the edges of the MST and the matching to form a multigraph
    multigraph = [[] for _ in range(n)]
    # for u, v, w in mst + matching:
    #     multigraph[u].append((v, w))
    #     multigraph[v].append((u, w))
    for u, v in mst + matching:
        print(u, v)
        w = euclidean_distance(coords[u], coords[v])
        multigraph[u].append((v, w))
        multigraph[v].append((u, w))

    # Step 6: Find an Eulerian circuit in the multigraph
    circuit = eulerian_circuit(multigraph, 0)

    # Step 7: Traverse the Eulerian circuit and skip repeated vertices to obtain a Hamiltonian cycle
    visited = [False] * n
    cycle = []
    for v in circuit:
        if not visited[v]:
            cycle.append(v)
               # Step 6: Find an Eulerian circuit in the multigraph
    circuit = eulerian_circuit(multigraph, 0)

    # Step 7: Traverse the Eulerian circuit and skip repeated vertices to obtain a Hamiltonian cycle
    visited = [False] * n
    cycle = []
    for v in circuit:
        if not visited[v]:
            cycle.append(v)
            visited[v] = True

    # Step 8: Calculate the total length of the Hamiltonian cycle
    length = sum(euclidean_distance(coords[cycle[i]], coords[cycle[i+1]]) for i in range(n-1))
    length += euclidean_distance(coords[cycle[-1]], coords[cycle[0]])

    return cycle, length


def plot_route(route: list):
    # poly: [(x0, y0), (x1, y1), (x2, y2)]
    fig = plt.figure()
    lines = [ [route[i], route[i+1]] for i in range(len(route)-1)]
    lines.append([route[-1], route[0]])
    lc = LineCollection(lines, colors="blue")

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.plot([points[i][0] for i in range(len(points))], [points[i][1] for i in range(len(points))], ".", color="black", alpha=0.6)
    ax.autoscale()
    plt.show()

# input
basename = sys.argv[-1].split(".")[0]

with open(basename+".tsp") as inputfile:
    try:
        indexofpoint = read_points(inputfile)
    except FileNotFoundError as err:
        print(err)

points = list(indexofpoint.keys())
cycle, length = christofides_tsp(points)
print("Hamiltonian cycle:", cycle)
print("Length:", length)

plot_route(cycle)
