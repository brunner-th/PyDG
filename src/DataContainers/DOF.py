import numpy as np

class DOF:
    def __init__(self, dof_num, node_num, element_num, coordinates):
        self.dof_num = dof_num
        self.node_num = node_num
        self.element_num = element_num
        self.coordinates = coordinates
        