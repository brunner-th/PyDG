import numpy as np


def LaxFriedrichsFlux(function: function, dir_derivative: list, a: float, b: float, n: np.array):

    f_star = np.mean(np.array([function(a), function(b)]), axis = 1) 

    u = np.linspace(a, b, 100)

    C = np.max(np.abs(n[0]*dir_derivative[0](u) + n[1]*dir_derivative[1](u)))

    f_star += C/2*n*(a-b)

    return f_star

