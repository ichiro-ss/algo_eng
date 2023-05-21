import sys
def output(algo, instance):
    if algo == "ls":
        points, ans, score, com_t = ls.main(instance)

    title = instance+"_"+algo
    # visualize
    # visualize.main(points, ans, title)

    # output results
    # print(_, ans)
    if instance == "berlin52":
        opt_v = 7542
    elif instance == "kroD100":
        opt_v = 21294
    elif instance == "d657":
        opt_v = 48912
    elif instance == "pr1002":
        opt_v = 259045
    elif instance == "d1655":
        opt_v = 62128
    elif instance == "pcb3038":
        opt_v = 137694
    elif instance == "rl5934":
        opt_v = 556045
    elif instance == "d15112":
        opt_v = 1573084

    print(algo, "score:", score, ", diff:", score - opt_v, "__", (score-opt_v)/opt_v * 100, "%")
    print("compute time: ", com_t, "sec")
    print()

filename = sys.argv[-1]
instances = []

with open("instances/"+filename+".txt") as inputfile:
    try:
        for line in inputfile.read().splitlines():
            if line:
                instances.append(line)
    except FileNotFoundError as err:
        print(err)

algos = []
for _ in instances:
    print(_)
    for algo in algos:
        output(algo, _)
