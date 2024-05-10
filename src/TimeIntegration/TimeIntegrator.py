import numpy as np
from enum import Enum


class TimeIntegrator:
    def __init__(self, TimeIntegrationScheme: Enum, number_timesteps: int, delta_t: float):
        self.TimeIntegrationScheme = TimeIntegrationScheme
        self.number_timesteps = number_timesteps
        self.delta_t = delta_t




    