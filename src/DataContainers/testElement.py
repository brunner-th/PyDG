import numpy as np
from Node import Node
from Element import Element

p1 = np.array([0,0])
p2 = np.array([0,1])
p3 = np.array([1,0])

n1 = Node(1, p1)
n2 = Node(2, p2)
n3 = Node(3, p3)

edges = np.array([[1,2], [1,3], [2, 3]])

nodelist = [n1, n2, n3]

e1 = Element(1, nodelist, edges)

print(e1.node_list)
print(e1.edges)
print(e1.element_number)

