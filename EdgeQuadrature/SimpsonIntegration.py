import numpy as np

class SimpsonIntegration:
    def __init__(self, function, x_edge, y_edge):
        self.function = function
        self.weights = np.array([1, 4, 1])/2
        transformation_matrix = np.array([[2,0], [1,1] ,[0,2]])
        self.x_positions = transformation_matrix @ x_edge
        self.y_positions = transformation_matrix @ y_edge
        self.ds = np.linalg.norm(np.array([x_edge[1]-x_edge[0], y_edge[1]-y_edge[0]]))

    def integrate(self):
        
        result = 0
        for ind, weight in enumerate(self.weights):
            result += weight * self.function(self.x_positions[ind], self.y_positions[ind])*self.ds
            
        return result