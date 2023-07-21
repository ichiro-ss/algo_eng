import numpy as np
import sys
import time
import random
import nna
from primitives import *

def iterated_ls(cycle, dists):
    cnt = 0
    while cnt < 10:


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
