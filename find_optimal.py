inp = "SULLULULL"
memory = []
out = []
for a in inp:
    memory.append(a)
    try:
        if memory[-2] == "U":
            scnd = memory.pop()
            memory.pop()
            frst = memory.pop()
            if frst == "L" and scnd == "L":
                memory.append("S")
            if frst == "S" and scnd == "L":
                memory.append("R")
            if frst == "L" and scnd == "S":
                memory.append("R")
    except:
        continue
print(memory)
