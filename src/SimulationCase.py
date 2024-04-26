import numpy as np
from SpatialIntegration.SpatialIntegrationScheme import SpatialIntegrationScheme
from TimeIntegration.TimeIntegrator import TimeIntegrator
from DataContainers.Mesh import Mesh

class SimulationCase:
    def __init__(self, Mesh: Mesh, SpatialIntegrationScheme: SpatialIntegrationScheme, TimeIntegrator: TimeIntegrator):
        self.mesh = Mesh
        self.spatial_scheme = SpatialIntegrationScheme
        self.time_scheme = TimeIntegrator
        self.mass_matrix
        self.stiffness_matrix
        self.force_vector


    #def initiate():

    #def assemble():
        
        
    def solve():

        A = None
        b = None

        return np.linalg.solve(A, b)

