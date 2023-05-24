import numpy as np
import time
import sys
from primitives import *

def farthest_insertion_tsp(cities, distance_matrix):
    n = len(cities)

    # Start with an arbitrary city as the initial tour
    initial_city = np.random.randint(n)
    tour = [initial_city]
    unvisited_cities = set(range(n))
    unvisited_cities.remove(initial_city)

    while unvisited_cities:
        # Find the city farthest from the current tour
        farthest_city = max(unvisited_cities, key=lambda city: min(distance_matrix[city][tour]))

        # Determine the position to insert the farthest city
        best_position = None
        best_increase = float('inf')
        for i in range(len(tour)):
            current_distance = distance_matrix[tour[i - 1]][tour[i]]
            increase = distance_matrix[farthest_city][tour[i]] + distance_matrix[farthest_city][tour[i - 1]] - current_distance
            if increase < best_increase:
                best_increase = increase
                best_position = i

        # Insert the farthest city into the tour
        tour.insert(best_position, farthest_city)
        unvisited_cities.remove(farthest_city)

    return tour

def main(instance):
    with open("instances/"+instance+".tsp") as inputfile:
        try:
            indexofpoint = read_points(inputfile)
        except FileNotFoundError as err:
            print(err)

    points = np.array(list(indexofpoint.keys()))
    distance_matrix = compute_distance_matrix(points)

    st = time.perf_counter()
    cycle = farthest_insertion_tsp(points, distance_matrix)
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

