import numpy as np
import matplotlib.pyplot as plt
import DataContainers.Mesh as Mesh
from Assembler.Assembler import Assembler
#import SimulationCase


mesh = Mesh.Mesh()
mesh.generate_basic_square_mesh(max_vol=0.1)
#mesh.plot_mesh()
mesh.fillNodeList()
mesh.fillElementList()
mesh.fillDOFList()
a1 = Assembler(mesh)
A,f = a1.assemble_total()

plt.imshow(A)
plt.show()

u = np.linalg.solve(A, f)
plt.tricontourf(mesh.triangles, u)
plt.show()








