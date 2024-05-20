import numpy as np
import matplotlib.pyplot as plt
import DataContainers.Mesh as Mesh
from Assembler.Assembler import Assembler
#import SimulationCase

alpha = -1
beta = 6
h = 0.25

mesh = Mesh.Mesh()
mesh.generate_basic_square_mesh(max_vol=h*h/2, min_angle=30)
#mesh.plot_mesh()
mesh.fillNodeList()
mesh.fillElementList()
mesh.fillDOFList()
mesh.fillEdgeList()
a1 = Assembler(mesh, h, alpha, beta)
A,f = a1.assemble_total()

#plt.imshow(A)

#f[0] = 100
#f[1] = 100
#f[2] = 100
u = np.linalg.solve(A, f)

ax = plt.figure().add_subplot(projection='3d')
#ax.tricontourf(mesh.getDOFPositions()[:,0], mesh.getDOFPositions()[:,1], u, 500, cmap='magma')
ax.plot_trisurf(mesh.getDOFPositions()[:,0], mesh.getDOFPositions()[:,1], u, triangles = mesh.getDOFTriangles(), cmap='magma', edgecolor='k')



plt.show()
print("Finished!")







