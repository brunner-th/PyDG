import numpy as np
from DataContainers.Node import Node
from DataContainers.DOF import DOF

class Element:
    def __init__(self, element_number: int, node_list: list[Node], edges: dict[int: list[Node, Node]]):
        self.element_number = element_number
        self.node_list = node_list
        self.dof_list = []
        self.edges =  edges
        self.number_edges = len(edges)
        self.neighbour_elements = None

    def addDOF(self, dof: DOF):
        self.dof_list.append(dof)



   

