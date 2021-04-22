from NewNeutron import NeuralNetwork
import numpy

with open("weights", "r") as file:
    weights = list(map(float, file.read().split("\n")))
file.close()
a = NeuralNetwork(weights=weights)

print(a.think(numpy.array([-0.2, -0.51, -0.16])))
