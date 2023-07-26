import numpy as np
import warnings
import sys
import time
import random
import nna
from primitives import *
import copy
import math
LIMIT = 100
warnings.filterwarnings('ignore')

def opt(cycle, sw1, sw2):
    rev = cycle[sw1:sw2+1]
    rev.reverse()
    cycle = cycle[:sw1]+rev+cycle[sw2+1:]

    return cycle

def simulated_annealing(cycle, dists):
    now_cycle = best_cycle = copy.copy(cycle)
    now_v = best_v = score(cycle, dists)
    t_st, t_fin = 50, 10
    n = len(cycle)
    move = 0

    st = time.perf_counter()
    while time.perf_counter() - st < LIMIT:
        sw1 = random.randrange(0, n-1)
        sw2 = random.randrange(sw1+1, n)
        sw1m = sw1-1 if sw1 else n-1
        sw2p = sw2+1 if sw2 != n-1 else 0
        if not ((sw1 == 0 and sw2 == n-1) or sw2 - sw1 == 1):
            diff = dists[cycle[sw1]][cycle[sw2p]] + dists[cycle[sw2]][cycle[sw1m]] - dists[cycle[sw1]][cycle[sw1m]] - dists[cycle[sw2]][cycle[sw2p]]
        else:
            diff = 0

        temp = t_st + (t_fin - t_st) * (time.perf_counter() - st) / LIMIT
        prob = 1 - np.exp(diff / temp)
        if prob > random.random():
            now_cycle = opt(cycle, sw1, sw2)
            now_v = score(now_cycle, dists)
        move += 1

    return best_cycle, move

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
    cycle, move = simulated_annealing(cycle, distance_matrix)
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
