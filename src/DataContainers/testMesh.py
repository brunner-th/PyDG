import numpy as np
import matplotlib.pyplot as plt
from Mesh import Mesh

max_volume = 10

mesh = Mesh()
mesh.initialize_basic_square_mesh()
mesh.plot_mesh()

print(mesh.points)

mesh.fillNodeList()

print(mesh.node_list)
print(mesh.facets)

mesh.fillElementList()

for element in mesh.element_list:
    for node in element.node_list:
        plt.plot(node.coordinates[0], node.coordinates[1], marker = ".", color = "k")

plt.show()

