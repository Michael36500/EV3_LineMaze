# xpole, ypole = 7, 5
# memory = []
# for _ in range(xpole):
#     temp = []
#     for _ in range(ypole):
#         tmp = []
#         for _ in range(4):
#             tmp.append(0)
#         temp.append(tmp)
#     memory.append(temp)


# def mprint():
#     global memory
#     for x in memory:
#         print(x)
# memory [0][1][2] = 1

# mprint()

import random



def make_decision(kriz):
    moznosti = {"U": ["U"], "L":["L"], "R":["R"], "J":["S", "L"], "K":["S","R"], "T":["R","L"], "+":["R","L","S"]}
    vyber = moznosti[kriz]
    
    if len(vyber) == 1: rand = 0
    else: rand = vyber[random.randint(0, len(vyber))]

    print(vyber, kriz)
    if rand == "R":
        print("right")
    if rand == "L":
        print("left")
    if rand == "S":
        print("strght")
    print()
make_decision("K")