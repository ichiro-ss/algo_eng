import numpy as np
import sys
import time
import random
import nna
from primitives import *
import ls_swop
import ls_opt
import copy

def double_b(cycle, dists):
    tcycle = copy.copy(cycle)
    i = random.randrange(0, len(cycle)-7)
    j = random.randrange(i+2, len(cycle)-5)
    k = random.randrange(j+2, len(cycle)-3)
    l = random.randrange(k+2, len(cycle)-1)
    tcycle[i+1:l+1] = tcycle[k+1:l+1] + tcycle[j+1:k+1] + tcycle[i+1:j+1]

    return tcycle

def iterated_ls(cycle, dists):
    cnt_kick = 0
    pre_score = score(cycle, dists)
    st = time.perf_counter()
    while time.perf_counter() - st < 100:
        tmp_cycle = double_b(cycle, dists)
        tmp_cycle, _ = ls_opt.local_search(tmp_cycle, dists)
        tmp_score = score(tmp_cycle, dists)
        if tmp_score < pre_score:
            cycle = tmp_cycle
            pre_score = tmp_score
        cnt_kick += 1

    return cycle, cnt_kick

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
    cycle, move = iterated_ls(cycle, distance_matrix)
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
