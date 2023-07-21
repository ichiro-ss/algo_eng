import numpy as np
import sys
import time
import random
import nna
from primitives import *
import copy

def swap(cycle, sw1, sw2):
    res = copy.copy(cycle)
    res[sw1] = cycle[sw2]
    res[sw2] = cycle[sw1]

    return res

def opt(cycle, sw1, sw2):
    rev = cycle[sw1:sw2+1]
    rev.reverse()
    cycle = cycle[:sw1]+rev+cycle[sw2+1:]

    return cycle

def local_search(cycle, dists):
    move = 0
    n = len(cycle)
    pre_score = score(cycle, dists)
    while True:
        # swap
        while True:
            st1, st2 = 0, 0
            changed = False
            end = 0
            for i in range(n):
                for j in range(i, n):
                    sw1, sw2 = st1+i if st1+i < n else st1+i-n, st2+j if st2+j < n else st2+j-n
                    if sw1 > sw2:
                        tmp = sw1
                        sw1 = sw2
                        sw2 = tmp
                    if sw1 == 0 and sw2 == n-1:
                        sw1 = n-1
                        sw2 = 0
                    sw1m = sw1-1 if sw1 else n-1
                    sw2m = sw2-1 if sw2 else n-1
                    sw1p = sw1+1 if sw1 != n-1 else 0
                    sw2p = sw2+1 if sw2 != n-1 else 0
                    if not ((sw1 == n-1 and sw2 == 0) or sw2 - sw1 == 1):
                        diff = \
                            dists[cycle[sw1]][cycle[sw2m]] + dists[cycle[sw1]][cycle[sw2p]]\
                            + dists[cycle[sw2]][cycle[sw1m]] + dists[cycle[sw2]][cycle[sw1p]]\
                            - dists[cycle[sw1]][cycle[sw1m]] - dists[cycle[sw1]][cycle[sw1p]]\
                            - dists[cycle[sw2]][cycle[sw2m]] - dists[cycle[sw2]][cycle[sw2p]]
                    else:   # wrong here
                        diff = \
                            dists[cycle[sw1]][cycle[sw2p]] + dists[cycle[sw2]][cycle[sw1m]]\
                            - dists[cycle[sw1]][cycle[sw1m]] - dists[cycle[sw2]][cycle[sw2p]]

                    if diff + 0.0001 < 0:
                        now_score = pre_score + diff
                        move += 1
                        # print("swap:", pre_score, "->", now_score, "|", sw1, "<->", sw2, sw1m, sw1p, sw2m, sw2p)
                        pre_score = now_score
                        st1, st2 = sw1, sw2
                        cycle = swap(cycle, sw1, sw2)
                        changed = True
                        end += 1
                        break
                else:
                    continue
                break
            if not changed:
                break

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

                    if diff + 0.0001 < 0:
                        now_score = pre_score + diff
                        move += 1
                        # print("opt:", pre_score, "->", now_score)
                        pre_score = now_score
                        st1, st2 = sw1, sw2
                        cycle = opt(cycle, sw1, sw2)
                        changed = True
                        end += 1
                        break
                else:
                    continue
                break

            if not changed:
                break
        if not end:
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
