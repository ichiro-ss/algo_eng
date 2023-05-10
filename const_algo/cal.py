import sys
import chatGPT

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
    print(_, ans)
    print("score:", score)
