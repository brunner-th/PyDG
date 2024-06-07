import numpy as np
import matplotlib.pyplot as plt
<<<<<<< Updated upstream
=======
import os
>>>>>>> Stashed changes
import DataContainers.Mesh as Mesh

<<<<<<< Updated upstream
#import SimulationCase


max_volume = 10

mesh = Mesh.Mesh()
mesh.initialize_basic_square_mesh()
=======
cwd = os.getcwd()
alpha = -1
beta = 8
h = 0.1 #0.25, 0.1, 0.05

mesh = Mesh.Mesh()
#mesh.generate_basic_square_mesh(max_vol=h*h/2, min_angle=30)
mesh.loadMesh(cwd+"/src/Meshes/sq_mesh_h_"+str(h).replace(".","")+".hdf5")
>>>>>>> Stashed changes
mesh.plot_mesh()









