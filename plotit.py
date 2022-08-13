from matplotlib import pyplot as plt

inp = [10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 4, 4, 4, 4, 4, 4, 4, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 10, 10, 10, 10, 10, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
rng = range(len(inp))

plt.plot(rng, inp)
plt.show()
