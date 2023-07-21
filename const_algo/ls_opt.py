import numpy as np
import sys
import time
import random
import nna
from primitives import *

def swap(cycle, sw1, sw2):
    tmp = cycle[sw1]
    cycle[sw1] = cycle[sw2]
    cycle[sw2] = tmp

def opt(cycle, sw1, sw2):
    rev = cycle[sw1:sw2+1]
    rev.reverse()
    cycle = cycle[:sw1]+rev+cycle[sw2+1:]

    return cycle

def local_search(cycle, dists):
    move = 0
    n = len(cycle)
    pre_score = score(cycle, dists)

    # 2-opt
    while True:
        st1 = 0
        changed = False
        for i in range(n):
            for j in range(i+1, n):
                sw1, sw2 = st1+i if st1+i < n else st1+i-n, st1+j if st1+j < n else st1+j-n
                if sw1 > sw2:
                    tmp = sw1
                    sw1 = sw2
                    sw2 = tmp
                sw1m = sw1-1 if sw1 else n-1
                sw2p = sw2+1 if sw2 != n-1 else 0
                if not ((sw1 == 0 and sw2 == n-1) or sw2 - sw1 == 1):
                    diff = dists[cycle[sw1]][cycle[sw2p]] + dists[cycle[sw2]][cycle[sw1m]] - dists[cycle[sw1]][cycle[sw1m]] - dists[cycle[sw2]][cycle[sw2p]]
                else:
                    diff = 0
                # now_score = score(tmp, dists)

                if diff + 0.0001 < 0:
                    now_score = pre_score + diff
                    # if score(tmp, dists) + 0.0001 > pre_score:
                    #     print("swap:", pre_score, "->", now_score)
                    #     print(score(cycle, dists), "true:", score(tmp, dists))
                    #     print(sw1m, sw1, sw2, sw2p)
                    #     print(pre_score, "-", dists[cycle[sw1]][cycle[sw1m]], "-", dists[cycle[sw2]][cycle[sw2p]]\
                    #           , "+", dists[cycle[sw1]][cycle[sw2p]], "+", dists[cycle[sw2]][cycle[sw1m]])
                    #     exit()
                    t = pre_score
                    move += 1
                    # print("opt", pre_score, "->", now_score)
                    pre_score = now_score
                    st1, st2 = sw1, sw2
                    cycle = opt(cycle, sw1, sw2)
                    changed = True
                    break
            else:
                continue
            break
        if not changed:
            break

    return cycle, move

def main(instance):
    with open("instances/"+instance+".tsp") as inputfile:
        try:
            indexofpoint = read_points(inputfile)
        except FileNotFoundError as err:
            print(err)

    points = np.array(list(indexofpoint.keys()))
    distance_matrix = compute_distance_matrix(points)

    cycle = nna.nearest_neighbor(points, distance_matrix)
    st = time.perf_counter()
    cycle, move = local_search(cycle, distance_matrix)
    en = time.perf_counter()

    return points, cycle, score(cycle, distance_matrix), en-st, move

if __name__ == "__main__":
    # input
    basename, extname = sys.argv[-1].split(".")
    if extname == "tsp":
        points, ans, sc, com_t = main(basename)
        print(basename, ans)
        print("score", sc)
    elif extname == "txt":
        with open("instances/"+basename+".txt") as inputfile:
            try:
                for line in inputfile.read().splitlines():
                    points, ans, sc, com_t = main(line)
                    print(line, ans)
                    print("score:", sc)
            except FileNotFoundError as err:
                print(err)
