import numpy as np
from Node import Node
 
class Element:
    def __init__(self, element_number: int, node_list: list[Node], edges: dict[int: list[Node, Node]]):
        self.element_number = element_number
        self.node_list = node_list
        self.edges =  edges
        self.number_edges = len(edges)

    

