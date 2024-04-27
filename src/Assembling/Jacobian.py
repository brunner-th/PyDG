import numpy as np

def determinate_Jacobian(p_i, p_j, p_k):
    return (p_j[0]-p_i[0])*(p_k[1]-p_i[1])-(p_k[0]-p_i[0])*(p_j[1]-p_i[1])