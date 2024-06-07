import numpy as np
import matplotlib.pyplot as plt
from Mesh import Mesh

max_volume = 10

mesh = Mesh()
mesh.generate_basic_square_mesh(max_vol=0.001)
mesh.plot_mesh()

print(mesh.points)

mesh.fillNodeList()

print(np.shape(mesh.node_list))
print(np.shape(mesh.facets))

mesh.fillElementList()

print(np.shape(mesh.element_list))

for element in mesh.element_list:
    for node in element.node_list:
        plt.plot(node.coordinates[0], node.coordinates[1], marker = ".", color = "k")


mesh.fillDOFList()

print(np.shape(mesh.dof_list))

plt.show()

mesh.fillDOFList()

