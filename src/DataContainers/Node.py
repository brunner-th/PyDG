import numpy as np

class Node:
    def __init__(self, node_number: int, coordinates: np.array):
        self.node_number = node_number
        self.coordinates =  coordinates
        self.dimension = np.shape(coordinates)[0]

    
