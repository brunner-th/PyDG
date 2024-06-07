import numpy as np

class BoundaryCondition:
    def __init__(self, dof_number_list: np.array, type: str, value: np.array):
        self.dof_number_list = dof_number_list
        self.type = type
        self.value = value

    