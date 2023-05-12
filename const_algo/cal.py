import sys
import chatGPT, two_approx

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
    ans, score = chatGPT.main(_)
    print("chatGPT")
    # print(_, ans)
    print("score:", score)
    ans, score = two_approx.main(_)
    print("2approx")
    # print(_, ans)
    print("score:", score)
