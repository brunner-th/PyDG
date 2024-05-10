import numpy as np
import matplotlib.pyplot as plt
import DataContainers.Mesh as Mesh
import Assembler.Assembler as Assembler
#import SimulationCase


mesh = Mesh.Mesh()
mesh.generate_basic_square_mesh(max_vol=0.001)
#mesh.plot_mesh()
mesh.fillNodeList()
mesh.fillElementList()
mesh.fillDOFList()
assembler = Assembler(mesh)
#assembler.assemble_total()







