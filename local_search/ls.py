import numpy as np
import sys
import time
import const_algo.nna as nna
from const_algo.primitives import *

def local_search():
    return

def main(instance):
    with open("instances/"+instance+".tsp") as inputfile:
        try:
            indexofpoint = read_points(inputfile)
        except FileNotFoundError as err:
            print(err)

    points = np.array(list(indexofpoint.keys()))
    distance_matrix = compute_distance_matrix(points)

    st = time.perf_counter()
    cycle = nna.nearest_neighbor(points, distance_matrix)
    cycle = local_search(cycle)
    en = time.perf_counter()

    return points, cycle, score(cycle, distance_matrix), en-st

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
