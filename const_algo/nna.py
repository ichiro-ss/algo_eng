import sys
import numpy as np

def main(instance):
    with open("instances/"+instance+".tsp") as inputfile:
        try:
            indexofpoint = read_points(inputfile)
        except FileNotFoundError as err:
            print(err)

    points = np.array(list(indexofpoint.keys()))

    cycle = solve_tsp_2approx(points)

    return cycle, eval_tsp(cycle, compute_distance_matrix(points))

if __name__ == "__main__":
    # input
    basename, extname = sys.argv[-1].split(".")
    if extname == "tsp":
        ans, score = main(basename)
        print(basename, ans)
        print("score", score)
    elif extname == "txt":
        with open("instances/"+basename+".txt") as inputfile:
            try:
                for line in inputfile.read().splitlines():
                    ans, score = main(line)
                    print(line, ans)
                    print("score:", score)
            except FileNotFoundError as err:
                print(err)
