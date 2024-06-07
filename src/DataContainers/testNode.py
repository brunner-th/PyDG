import numpy as np
from Node import Node
from DOF import DOF


n1 = Node(1, np.array([0,1]))
n2 = Node(2, np.array([3,2,1]))

print(n1.coordinates)
print(n1.dimension)
print(n1.node_number)

print(n2.coordinates)
print(n2.dimension)

d1 = DOF(1, np.array([0,1]))
d2 = DOF(2, np.array([3,2]))

n1.addDOF(d1)
n1.addDOF(d2)

print(n1.dof_list)