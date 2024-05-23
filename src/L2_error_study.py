import numpy as np
import matplotlib.pyplot as plt
import os
import time

import DataContainers.Mesh as Mesh
from Assembler.Assembler import Assembler

cwd = os.getcwd()

alpha = -1
beta_list = [4,10,20,40,80]
h_list = [0.25, 0.1, 0.05]

L2_error = np.zeros((len(h_list), len(beta_list)))
fig_m, axs_m = plt.subplots(1, len(h_list), figsize=(10,5))
fig, axs = plt.subplots(len(beta_list),len(h_list), figsize=(10,15), subplot_kw=dict(projection='3d'), layout = "constrained")
axs[0,0].set_title("h = 0.25")
axs[0,1].set_title("h = 0.1")
axs[0,2].set_title("h = 0.05")


x_anal = np.linspace(0, 1, 100)
y_anal = np.linspace(0, 1, 100)
xx, yy = np.meshgrid(x_anal, y_anal)

def anal_sol(x, y):
    return np.sin(np.pi*x)*np.sin(np.pi*y)

u_anal = anal_sol(xx, yy)

for i, h in enumerate(h_list):
    
    print("processing h = ", h)
    mesh = Mesh.Mesh()
    mesh.loadMesh(cwd+"/src/Meshes/sq_mesh_h_"+str(h).replace(".","")+".hdf5")
    mesh.plot_mesh(axs_m[i])
    mesh.fillNodeList()
    mesh.fillElementList()
    mesh.fillDOFList()
    mesh.fillEdgeList()
    print("created mesh")
    for j, beta in enumerate(beta_list):

        a1 = Assembler(mesh, h, alpha, beta)
        A,f = a1.assemble_total()
        u = np.linalg.solve(A, f)

        axs[j, i].plot_trisurf(mesh.getDOFPositions()[:,0], mesh.getDOFPositions()[:,1], u, triangles = mesh.getDOFTriangles(), cmap='magma', edgecolor='k')
        axs[j, i].plot_surface(xx, yy, u_anal, color="gray", linewidth=0.1, antialiased = True,  alpha=0.7)

        x_coords = mesh.getDOFPositions()[:,0]
        y_coords = mesh.getDOFPositions()[:,1]
        u_l2_anal = anal_sol(x_coords, y_coords)
        L2_error[i,j] = np.sqrt(np.sum((u - u_l2_anal)**2))


plt.show()


alpha = -1
beta_list = np.linspace(2, 100, 30)
h_list = [0.25, 0.1, 0.05]
L2_error = np.zeros((len(h_list), len(beta_list)))
elapsed_time = np.zeros((len(h_list), len(beta_list)))

for i, h in enumerate(h_list):
    
    print("processing h = ", h)
    mesh = Mesh.Mesh()
    mesh.loadMesh(cwd+"/src/Meshes/sq_mesh_h_"+str(h).replace(".","")+".hdf5")
    mesh.fillNodeList()
    mesh.fillElementList()
    mesh.fillDOFList()
    mesh.fillEdgeList()
    print("created mesh")
    for j, beta in enumerate(beta_list):

        start = time.time()
        a1 = Assembler(mesh, h, alpha, beta)
        A,f = a1.assemble_total()
        u = np.linalg.solve(A, f)
        end = time.time()

        x_coords = mesh.getDOFPositions()[:,0]
        y_coords = mesh.getDOFPositions()[:,1]
        u_l2_anal = anal_sol(x_coords, y_coords)
        L2_error[i,j] = np.sqrt(np.sum((u - u_l2_anal)**2))
        elapsed_time[i,j] = end-start


figl2, axl2 = plt.subplots(1, 2, figsize=(10,5), layout = "constrained")


for i, h in enumerate(h_list):
    axl2[0].semilogy(beta_list, L2_error[i,:], label = "h = "+str(h))
    axl2[1].plot(beta_list, elapsed_time[i,:], label = "h = "+str(h))

axl2[0].set_xlabel("beta")
axl2[0].set_ylabel("L2 error")
axl2[0].legend()
axl2[1].set_xlabel("beta")
axl2[1].set_ylabel("time")
axl2[1].legend()

plt.show()

print("Finished!")