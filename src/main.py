import numpy as np
import matplotlib.pyplot as plt

import DataContainers.Mesh as Mesh
from Assembler.Assembler import Assembler

alpha = -1
beta = 8
h = 0.1

mesh = Mesh.Mesh()
mesh.generate_basic_square_mesh(max_vol=h*h/2, min_angle=30)
mesh.plot_mesh()
mesh.fillNodeList()
mesh.fillElementList()
mesh.fillDOFList()
mesh.fillEdgeList()
a1 = Assembler(mesh, h, alpha, beta)
A,f = a1.assemble_total()
u = np.linalg.solve(A, f)

ax = plt.figure().add_subplot(projection='3d')
ax.plot_trisurf(mesh.getDOFPositions()[:,0], mesh.getDOFPositions()[:,1], u, triangles = mesh.getDOFTriangles(), cmap='magma', edgecolor='k')

x_anal = np.linspace(0, 1, 100)
y_anal = np.linspace(0, 1, 100)
xx, yy = np.meshgrid(x_anal, y_anal)
u_anal = np.sin(np.pi*xx)*np.sin(np.pi*yy)

ax.plot_surface(xx, yy, u_anal, color="gray",
                       linewidth=0.1, antialiased = True,  alpha=0.7)


plt.show()
print("Finished!")







