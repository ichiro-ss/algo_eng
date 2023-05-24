import sys
import numpy as np
from primitives import *
import time

def nearest_neighbor(points, dists):
    n = len(points)
    now_point = 0
    is_visited = [False]*len(points)
    is_visited[now_point] = True
    cycle = [now_point]

    for _ in range(n-1):
        min_idx = 0
        idx = 0
        while idx < n:
            if not is_visited[idx]:
                min_idx = idx
                break
            idx += 1

        for i in range(idx, n, 1):
            if not is_visited[i] and \
                dists[now_point][i] < dists[now_point][min_idx]:
                min_idx = i
        is_visited[min_idx] = True
        now_point = min_idx
        cycle.append(now_point)

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
    cycle = nearest_neighbor(points, distance_matrix)
    en = time.perf_counter()

    return points, cycle, score(cycle, distance_matrix), en-st

if __name__ == "__main__":
    # input
    basename, extname = sys.argv[-1].split(".")
    if extname == "tsp":
        points, ans, score, com_t = main(basename)
        print(basename, ans)
        print("score", score)
    elif extname == "txt":
        with open("instances/"+basename+".txt") as inputfile:
            try:
                for line in inputfile.read().splitlines():
                    points, ans, score, com_t = main(line)
                    print(line, ans)
                    print("score:", score)
            except FileNotFoundError as err:
                print(err)
