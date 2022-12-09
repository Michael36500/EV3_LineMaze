import numpy as np
from matplotlib import pyplot as plt
read = open("najeto_na_kolech2.txt")
read = read.readlines()

cisla = np.array([], dtype="int32")
for x in read:
    y = x.split()
    a = int(y[0])
    b = int(y[1])
    # cisla.append([a, b])
    cisla = np.append(cisla, (a,b))
cisla = cisla.reshape((260,2))
# print(cisla)
