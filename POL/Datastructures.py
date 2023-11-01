#%%
from Libraries import *

# %%
# Mass class
class Mass:
    def __init__(self, m, p, p_0 = np.zeros(3)):
        self.m = m
        self.p = np.array(p) + p_0
        self.v = np.array([0, 0, 0], dtype=np.float64)
        self.a = np.array([0, 0, 0], dtype=np.float64)

# Spring class
class Spring:
    def __init__(self, m1, m2, k):
        self.m1 = m1
        self.m2 = m2
        self.k = k
        self.L0 = np.linalg.norm(m1.p - m2.p)

# Cube class
class Cube:
    def __init__(self, cube_size=0.1, p_0= np.dot([0, 0, 1], 0.2), mass_value=0.1, k_value=10000):
        # Initialize vertices
        vertices = [
            np.dot([0, 0, 0.], cube_size), np.dot([1, 0, 0.], cube_size),
            np.dot([1, 1, 0.], cube_size), np.dot([0, 1, 0.], cube_size),
            np.dot([0, 0, 1.], cube_size), np.dot([1, 0, 1.], cube_size),
            np.dot([1, 1, 1.], cube_size), np.dot([0, 1, 1.], cube_size)
        ]

        # Initialize masses
        self.masses = [Mass(mass_value, v, p_0=p_0) for v in vertices]

        # Initialize springs
        self.springs = []
        for i, m1 in enumerate(self.masses):
            for j, m2 in enumerate(self.masses[i + 1:]):
                self.springs.append(Spring(m1, m2, k_value))

