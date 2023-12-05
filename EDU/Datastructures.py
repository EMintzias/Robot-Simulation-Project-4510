# %%
from Libraries import *
import random
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
        
    def __str__(self):
        out = f'Mass at Pos = {self.p}'
        out += f'\nMass vel = {self.v}'
        out += f'\nMass acc = {self.a}'
        #print(out)
        return out

# Spring class
class Spring:
    def __init__(self, m1, m2, k, b=0, c=0, tissue_type = None):
        self.m1 = m1
        self.m2 = m2
        self.L0 = np.linalg.norm(m1.p - m2.p)
        self.center = (m1.p+m2.p) /2
        self.tissue_type = tissue_type
        self.k = k
        self.b = b
        self.c = c
        
    def update_center(self):
        self.center = (self.m1.p+self.m2.p)/2   

        

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

'''
class Custom_body_1:
    def __init__(self, cube_size=0.1,  mass_value=0.1, k_value=9000, p_0=np.dot([0, 0, 0], 0.0), Genome_size = 8, prev_genome=None, only_bounce=False):
        self.fitness = 1e-7
        self.only_bounce = only_bounce
        
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

        if prev_genome is not None:
            self.genome = prev_genome
            for i in range(len(self.genome)):
                self.genome[i][0] += p_0
        else:
            self.genome = np.array([[pt , self.tissue_dict[np.random.choice([1,2,3,4])]] for pt in genome_points ])
        
        self.COM_update()
        self.Update_springs()

    def fuck_you(self):
        print('fuck you')
        
        
    def COM_update(self):
        rslt = np.zeros(3)
        total_mass = 0
        for mass in self.masses:
            rslt  += mass.p * mass.m
            total_mass += mass.m
        self.COM = rslt/total_mass
        return rslt/total_mass   
    
    
    def Update_springs(self):
        print('fuck')
        for s in self.springs:
            s.update_center() #should not be necessary since this is called after initialized but more robust here
            dist = [np.linalg.norm(s.center - g_pt) for g_pt in self.genome[:,0]]
            min_ind = np.argmin(dist)
            s.tissue_type = self.reverse_tissue_dict[tuple(self.genome[min_ind,1])]
            if self.only_bounce:
                s.k,s.b,s.c = self.genome[min_ind,1][0], 0, self.genome[min_ind,1][1]
                #s.b = 0
            else:
                s.k,s.b,s.c = self.genome[min_ind,1]
            
            pass
'''

class RandomBody:
    def __init__(self, cube_size=0.1,  mass_value=0.1, k_value=9000, p_0=np.array([0,0,0]), Genome_size = 8, prev_genome=None, only_bounce=False):
        self.fitness = 1e-7
        self.only_bounce = only_bounce
        
        # maps to properties (k,b,c)
        self.tissue_dict = {1:(1000,0,0), 2:(20000,0,0), 3:(5000,.125,0), 4:(5000,-.125,0)}
        self.reverse_tissue_dict = {value: key for key, value in self.tissue_dict.items()}
        self.has_been_mutated = False

        points = self.generate_points()
        #np.genfromtxt("table_body.txt", delimiter=',')

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

        self.og_masses = copy.deepcopy(self.masses)
        
        if prev_genome is not None:
            self.genome = prev_genome
            for i in range(len(self.genome)):
                self.genome[i][0] += p_0
        else:
            self.randomize_genome(Size = Genome_size)   
        
        self.COM_update()
        self.Update_springs()

        self.update_og_springs()
        
    
    def update_og_springs(self):
        og_springs = []
        for spring in self.springs:
            og_s = Spring(self.og_masses[self.masses.index(spring.m1)], self.og_masses[self.masses.index(spring.m2)], 
                          spring.k, b=spring.b, c=spring.c, tissue_type = spring.tissue_type)
            og_springs.append(og_s)
        self.og_springs = og_springs

    # TODO what happens when we mutate morphology?
    # TODO og_masses are not the same anymore, so keep track of deeper changes in og_masses, as well
    # TODO springs may also change, so we should keep a copy?
    def reset_body_position(self):
        self.masses.clear()
        self.masses.extend(self.og_masses)
        self.og_masses = copy.deepcopy(self.masses)
        self.springs.clear()
        self.springs.extend(self.og_springs)
        self.COM_update()
        self.Update_springs()
        self.update_og_springs()

    def checker(self):
        print(self.og_masses.index(self.og_springs[100].m1))

    def randomize_genome(self,Size = 8):   
        #Genome is a set of points with a corresponding tuple of properties (K,b,c)
        genome_points = [m.p for m in np.random.choice(self.masses, size=Size, replace=False)]
        self.genome = np.array([[pt , self.tissue_dict[np.random.choice([1,2,3,4])]] for pt in genome_points ])
        pass
    
    def generate_points(self, num_points=60, x_range=[0,5], y_range=[0,5], z_range=[0,5]):
        points = set()
        points.add((0, 0, 0))  # Start with the initial point
        while len(points) < num_points:
            # Randomly select an existing point
            existing_point = random.choice(list(points))
            # Generate a neighboring point
            dx, dy, dz = random.choice([(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1)])
            new_point = (existing_point[0] + dx, existing_point[1] + dy, existing_point[2] + dz)
            # Check if the new point is within the specified ranges and not already in points
            if (x_range[0] <= new_point[0] <= x_range[1] and
                y_range[0] <= new_point[1] <= y_range[1] and
                z_range[0] <= new_point[2] <= z_range[1] and
                new_point not in points):
                points.add(new_point)
        return np.array(list(points))

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
            if not self.has_been_mutated:
                s.tissue_type = self.reverse_tissue_dict[tuple(self.genome[min_ind,1])]
            if self.only_bounce:
                s.k,s.b,s.c = self.genome[min_ind,1][0], 0, self.genome[min_ind,1][1]
                #s.b = 0
            else:
                s.k,s.b,s.c = self.genome[min_ind,1]
            
            pass
        
    def Body_deep_copy(self):
        return copy.deepcopy(self)
    
    def Mutate_genome(self, mutation_size = .10, Position = False,
                      Tissue_mutation = True, Tissue_prob = 0.25):
        #recall genmoe are a set of tissue type centroids in the form of [ [[pos] [tissue]] for each centroid  ]
        # the below randomizes each if told to. 
        if Position:
            #selects a random ind in the genome and changes that position by the size
            ind = np.random.choice(np.arange(len(self.genome)))
            self.genome[ind][0]  += np.random.choice([-1,1])* mutation_size * self.genome[ind][0]
            
        
        if Tissue_mutation and np.random.rand() < Tissue_prob : 
            #will happen only ~25% even if told to by default
            ind = np.random.choice(np.arange(len(self.genome)))
            # Mutate k
            if np.random.rand() < 0.5:
                self.genome[ind][1][0] += np.random.choice([1,-1])*mutation_size*self.genome[ind][1][0]
            # Mutate b
            if np.random.rand() < 0.5:
                self.genome[ind][1][1] += np.random.choice([1,-1])*mutation_size*self.genome[ind][1][1]
            # Mutate c
            if np.random.rand() < 0.5:
                self.genome[ind][1][2] += np.random.choice([1,-1])*mutation_size
            
            if self.has_been_mutated == False:
                self.has_been_mutated = True
            
            self.Update_springs()

            #self.genome[ind][1] = self.tissue_dict[np.random.choice([1,2,3,4])]
            
        return 
    
def Main():
    B = RandomBody(Genome_size=3)
    #print(B.genome)
    B.reset_body_position()
    B.checker()
    #B.Mutate_genome(Tissue_prob=1)
    #print('\n ------------\n', B.genome)

if __name__ == "__main__":
    Main()


   
   #print(table.reverse_tissue_dict)
   #print(table.springs[0].center)
