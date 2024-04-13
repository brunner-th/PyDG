import numpy as np
import SpatialIntegrator
import TimeIntegrator

class SimulationCase:
    def __init__(self, Mesh, SpatialIntegrationScheme, TimeIntegrator):
        self.mesh = Mesh
        self.spatial_scheme = SpatialIntegrationScheme
        self.time_scheme = TimeIntegrator