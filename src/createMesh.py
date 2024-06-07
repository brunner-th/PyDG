import numpy as np
import matplotlib.pyplot as plt
import os
import DataContainers.Mesh as Mesh

cwd = os.getcwd()

h = 0.05

mesh = Mesh.Mesh()
mesh.generate_basic_square_mesh(max_vol=h*h/2, min_angle=30)
print("generated")
mesh.saveMesh(cwd+"/src/Meshes/sq_mesh_h_005.hdf5")