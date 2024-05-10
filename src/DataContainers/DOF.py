import numpy as np

class DOF:
    def __init__(self, dof_number: int, position: np.array, node_number: int):
        self.position = position
        self.dof_number = dof_number
        self.node_number = node_number

