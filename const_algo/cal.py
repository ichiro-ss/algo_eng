import sys
import chatGPT, two_approx, nna

filename = sys.argv[-1]
instances = []

with open("instances/"+filename+".txt") as inputfile:
    try:
        for line in inputfile.read().splitlines():
            if line:
                instances.append(line)
    except FileNotFoundError as err:
        print(err)

for _ in instances:
    ans, score, com_t = chatGPT.main(_)
    print(_)
    # print(_, ans)
    print("chatGPT score:", score)
    print("compute time: ", com_t, "sec")
    print()
    ans, score, com_t = two_approx.main(_)
    # print(_, ans)
    print("2approx score:", score)
    print("compute time: ", com_t, "sec")
    print()

    ans, score, com_t = nna.main(_)
    # print(_, ans)
    print("NNA|n^2 score:", score)
    print("compute time: ", com_t, "sec")
    print()
