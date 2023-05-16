import sys
import chatGPT, two_approx, nna
import visalize

def output(algo, instance):
    if algo == "chatGPT":
        points, ans, score, com_t = chatGPT.main(instance)
    elif algo == "2approx":
        points, ans, score, com_t = two_approx.main(instance)
    elif algo == "NNA|n^2":
        points, ans, score, com_t = nna.main(instance)

    title = instance+"_"+algo
    # visualize
    visalize.main(points, ans, title)

    # output results
    # print(_, ans)
    print(algo, "score:", score)
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

algos = ["chatGPT", "2approx", "NNA|n^2"]
for _ in instances:
    print(_)
    for algo in algos:
        output(algo, _)
