# %%
from Libraries import *
from dtypes import *

#%%
# Mass class
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
    def __init__(self, m1, m2, k, tissue_type = None):
        self.m1 = m1
        self.m2 = m2
        self.L0 = np.linalg.norm(m1.p - m2.p)
        self.center = (m1.p+m2.p) /2
        
        self.tissue_type = tissue_type
        self.k = k
        self.b = 0
        self.c = 0
        
    def update_center(self):
        self.center = (self.m1.p+self.m2.p)/2   




class Cube_jit:
    def __init__(self, cube_size=0.1, p_0=np.array([0, 0, 1]), mass_value=0.1, k_value=10000):
        # Initialize vertices
        vertices = [
            np.array([0, 0, 0.]) * cube_size, np.array([1, 0, 0.]) * cube_size,
            np.array([0, 1, 0.]) * cube_size, np.array([1, 1, 0.]) * cube_size,
            np.array([0, 0, 1.]) * cube_size, np.array([1, 0, 1.]) * cube_size,
            np.array([0, 1, 1.]) * cube_size, np.array([1, 1, 1.]) * cube_size
        ]

        # Initialize masses and springs arrays
        self.masses = np.zeros(len(vertices), dtype=mass_dtype)
        for i, v in enumerate(vertices):
            self.masses[i]['m'] = mass_value
            self.masses[i]['p'] = v + p_0
            self.masses[i]['v'] = np.zeros(3, dtype=np.float64)
            self.masses[i]['a'] = np.zeros(3, dtype=np.float64)

        # Initialize springs
        # Assuming self.springs will be populated with appropriate logic
        self.springs = np.zeros(0, dtype=spring_dtype)  # Replace NUM_SPRINGS with actual count

        # Populate springs array
        # ...

        # Initialize faces for PyOpenGL plotting - this will need to be adjusted if using NumPy arrays
        self.faces = [
            [self.masses[i] for i in [0, 1, 3, 2]],
            [self.masses[i] for i in [4, 5, 7, 6]],
            [self.masses[i] for i in [0, 4, 6, 2]],
            [self.masses[i] for i in [1, 5, 7, 3]],
            [self.masses[i] for i in [0, 1, 5, 4]],
            [self.masses[i] for i in [2, 3, 7, 6]]
        ]

        # Compute the center of mass
        self.COM_update()

    def COM_update(self):
        total_mass = np.sum(self.masses['m'])
        weighted_positions = self.masses['p'].T * self.masses['m']
        self.COM = np.sum(weighted_positions, axis=1) / total_mass



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
                spring = Spring(m1, m2, k_value, tissue_type = 1)
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
                                spring = Spring(mass1, mass2, k_value, tissue_type = 1)
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
    def __init__(self, cube_size=0.1,  mass_value=0.1, k_value=9000, p_0=np.dot([0, 0, 0], 0.0),
                 Genome_size = 8) -> None:
        self.fitness = 1e-7
        
        # maps to properties (k,b,c)
        self.tissue_dict = {1:(1000,0,0), 2:(20000,0,0), 3:(5000,.125,0), 4:(5000,-.125,0)}
        self.reverse_tissue_dict = {value: key for key, value in self.tissue_dict.items()}

        points = np.genfromtxt("table_body.txt", delimiter=',')
        #self.masses = np.zeros((len(points),3))
        masses_dict = defaultdict(lambda: None)
        
        for i,point in enumerate(points):
            masses_dict[tuple(point)] = Mass(mass_value, point * cube_size, p_0=p_0)
            
        self.masses = list(masses_dict.values())

        springs =[]
        for point in points:
            x,y,z = point
            cube_masses = [masses_dict[(x+dx, y+dy, z+dz)] for dx in range(2) for dy in range(2) for dz in range(2)]
            cube_masses = [mass for mass in cube_masses if mass is not None]
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
        
        
        #Genome is a set of points with a corresponding tuple of properties (K,b,c)
        genome_points = [m.p for m in np.random.choice(self.masses, size=Genome_size, replace=False)]

        
        self.genome = np.array([[pt , self.tissue_dict[np.random.choice([1,2,3,4])]] for pt in genome_points ])
        self.COM_update()
        self.Update_springs()
        print('fuck jit')
        
        
    def COM_update(self):
        rslt = np.zeros(3)
        total_mass = 0
        for mass in self.masses:
            rslt  += mass.p * mass.m
            total_mass += mass.m
        self.COM = rslt/total_mass
        return rslt/total_mass   
    
    
    def Update_springs(self):
        for s in self.springs:
            s.update_center() #should not be necessary since this is called after initialized but more robust here
            dist = [np.linalg.norm(s.center - g_pt) for g_pt in self.genome[:,0]]
            min_ind = np.argmin(dist)
            s.k,s.b,s.c = self.genome[min_ind,1]
            s.tissue_type = self.reverse_tissue_dict[tuple(self.genome[min_ind,1])]
            pass
            

if __name__ == "__main__":
   table = Custom_body_1()
   #print(table.reverse_tissue_dict)
   #print(table.springs[0].center)

# %%
#lattice = CubeLattice(lattice_size=2, k_value=9000, p_0 = [0,0,0])
#print(lattice.genome)


