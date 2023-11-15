# %%
#from Libraries import *
# Mass class
import numpy as np
class Mass:
    def __init__(self, m, p, p_0 = np.zeros(3)):
        self.m = m
        self.p = np.array(p) + p_0
        self.v = np.array([0, 0, 0], dtype=np.float64)
        self.a = np.array([0, 0, 0], dtype=np.float64)
        self.springs = []

    def add_spring(self, spring):
        self.springs.append(spring)

# Spring class
class Spring:
    def __init__(self, m1, m2, k):
        self.m1 = m1
        self.m2 = m2
        self.k = k
        self.L0 = np.linalg.norm(m1.p - m2.p)

# Cube class
class Cube:
    def __init__(self, cube_size=0.1, p_0=np.dot([0, 0, 1], 0.0), mass_value=0.1, k_value=10000):
        # Initialize vertices
        vertices = [
            np.dot([0, 0, 0.], cube_size), np.dot([1, 0, 0.], cube_size),
            np.dot([0, 1, 0.], cube_size), np.dot([1, 1, 0.], cube_size),
            np.dot([0, 0, 1.], cube_size), np.dot([1, 0, 1.], cube_size),
            np.dot([0, 1, 1.], cube_size), np.dot([1, 1, 1.], cube_size)
        ]

        # Initialize masses
        self.masses = [Mass(mass_value, v, p_0=p_0) for v in vertices]

        # Initialize springs
        self.springs = []
        for i, m1 in enumerate(self.masses):
            for j, m2 in enumerate(self.masses[i + 1:]):
                spring = Spring(m1, m2, k_value)
                self.springs.append(spring)
                m1.add_spring(spring)
                m2.add_spring(spring)

        # Initialize faces for PyOpenGL plotting
        self.faces = [
            [self.masses[i] for i in [0, 1, 3, 2]],
            [self.masses[i] for i in [4, 5, 7, 6]],
            [self.masses[i] for i in [0, 4, 6, 2]],
            [self.masses[i] for i in [1, 5, 7, 3]],
            [self.masses[i] for i in [0, 1, 5, 4]],
            [self.masses[i] for i in [2, 3, 7, 6]]
        ]
        self.COM_update()
        
        
    def COM_update(self):
        rslt = np.zeros(3)
        total_mass = 0
        for mass in self.masses:
            rslt  += mass.p * mass.m
            total_mass += mass.m
        self.COM = rslt/total_mass
        return rslt/total_mass

# Cube Lattice class
class CubeLattice:
    def __init__(self, cube_size=0.1, lattice_size=3, mass_value=0.1, k_value=9000, p_0=np.dot([0, 0, 1], 0.0)):
        # Create a dictionary to hold all masses
        masses = {}
        for x in range(lattice_size + 1):
            for y in range(lattice_size + 1):
                for z in range(lattice_size + 1):
                    position = np.array([x, y, z]) * cube_size
                    masses[(x, y, z)] = Mass(mass_value, position, p_0=p_0)
        self.masses = list(masses.values())

        # Create a list to hold all springs
        springs = []
        # Connect masses with springs within each cube
        for x in range(lattice_size):
            for y in range(lattice_size):
                for z in range(lattice_size):
                    # Iterate over all pairs of masses within a single cube
                    cube_masses = [masses[(x+dx, y+dy, z+dz)] for dx in range(2) for dy in range(2) for dz in range(2)]
                    for i, mass1 in enumerate(cube_masses):
                        for mass2 in cube_masses[i+1:]:
                            # Check if a spring already exists between these two masses
                            if not any(spring.m1 == mass1 and spring.m2 == mass2 or 
                                    spring.m1 == mass2 and spring.m2 == mass1 for spring in mass1.springs):
                                spring = Spring(mass1, mass2, k_value)
                                springs.append(spring)
                                mass1.add_spring(spring)
                                mass2.add_spring(spring)
        self.springs = springs 
        self.COM_update()
        self.fitness = 1e-7
        
    def COM_update(self):
        rslt = np.zeros(3)
        total_mass = 0
        for mass in self.masses:
            rslt  += mass.p * mass.m
            total_mass += mass.m
        self.COM = rslt/total_mass
        return rslt/total_mass


class Custom_body_1:
    def __init__(self) -> None:
        self.fitness = 1e-7
        self.genome = np.ones(5)

        points = np.genfromtxt("table_body.txt", delimiter=',')
        self.masses = np.zeros((len(points),3))
        
        for i in range(points.size):
            self.masses[i] = 
        
        
        self.COM_update()
        
        
    def COM_update(self):
        rslt = np.zeros(3)
        total_mass = 0
        for mass in self.masses:
            rslt  += mass.p * mass.m
            total_mass += mass.m
        self.COM = rslt/total_mass
        return rslt/total_mass   
        
        
        
        
        pass
            


# %%
lattice = CubeLattice(lattice_size=2, k_value=9000, p_0 = [0,0,0])
for mass in lattice.masses:
    print(mass.p)

