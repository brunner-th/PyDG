import numpy as np

class LinearBasisFunction:
    
    def evaluateLinearBasisFunction(self, x_nodes, y_nodes, eval_x, eval_y):
        V = np.array([np.full_like(x_nodes, 1), x_nodes, y_nodes]) 
        A = np.linalg.solve(V, np.diag([1, 1, 1]))
        a = A[:,0]
        b = A[:,1]
        c = A[:,2]
        value = a+b*eval_x+c*eval_y
        return value, a, b, c
    
    def evaluateValueLinearBasisFunction(self, x_nodes, y_nodes, eval_x, eval_y):
        V = np.array([np.full_like(x_nodes, 1), x_nodes, y_nodes])
        A = np.linalg.solve(V, np.diag([1, 1, 1]))
        a = A[:,0]
        b = A[:,1]
        c = A[:,2]
        value = a+b*eval_x+c*eval_y
        return value
    
    def evalulateGradientsLinearBasisFunction(self, x,y):
        area = 0.5 * abs((x[0] * (y[1] - y[2]) + x[1] * (y[2] - y[0]) + x[2] * (y[0] - y[1])))
        b = np.array([y[1]-y[2], y[2]-y[0], y[0]-y[1]])/(2*area)
        c = np.array([x[2]-x[1], x[0]-x[2], x[1]-x[0]])/(2*area)

        return area, b, c


