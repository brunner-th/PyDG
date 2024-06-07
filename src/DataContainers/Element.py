import numpy as np
from DataContainers.Node import Node
from DataContainers.DOF import DOF
from DataContainers.Edge import Edge

class Element:
    def __init__(self, element_number: int, node_list: "list[Node]"):
        self.element_number = element_number
        self.node_list = node_list
        self.node_num_list = [node.node_number for node in node_list]
        self.dof_list = []
        self.edge_list = []
        self.neighbour_elements = None

    def addDOF(self, dof: DOF):
        self.dof_list.append(dof)

    def addEdge(self, edges: Edge):
        self.edge_list.append(edges)




   

