#%%
from Libraries import *
from Datastructures import *

cube_size=0.1
lattice_size=3
mass_value=0.1
k_value=10000

# Create a grid of masses
masses = {}
for x in range(lattice_size + 1):
    for y in range(lattice_size + 1):
        for z in range(lattice_size + 1):
            position = np.array([x, y, z]) * cube_size
            masses[(x, y, z)] = Mass(mass_value, position)

print(len(masses))

#%%
for i, mass in enumerate(cube.masses):
            # Initial force is 0
            F = np.zeros(3)
            # SPRING FORCE
            # Loop over all springs
            for spring in cube.springs:
                # If spring connected to that mass
                if spring.m1 == mass or spring.m2 == mass:
                    # Calculate spring force
                    L = np.linalg.norm(spring.m1.p - spring.m2.p)
                    # Update F_spring in the vector direction from m2 to m1
                    F_spring = spring.k * (L - spring.L0) * (spring.m1.p - spring.m2.p) / L
                    # Update F with appropriate sign
                    if spring.m1 == mass:
                        F -= F_spring
                    else:
                        F += F_spring
            # GRAVITATIONAL FORCE
            # Update F
            F += mass.m * g
            # GROUND COLLISION FORCE
            # Ground collision check and response
            if mass.p[2] < 0:
                F += np.array([0, 0, -kc * mass.p[2]])
            # UPDATE ACCELERATION
            mass.a = F / mass.m
            # UPDATE VELOCITY
            mass.v += mass.a * dt
            mass.v *= b
            # UPDATE POSITION
            mass.p += mass.v * dt



# %%
# Loop over all springs
            for spring in cube.springs:
                # If spring connected to that mass
                if spring.m1 == mass or spring.m2 == mass:
                    # Calculate spring force
                    L = np.linalg.norm(spring.m1.p - spring.m2.p)
                    F_spring = spring.k * (L - spring.L0)
                    # Update F_spring in the vector direction from m2 to m1
                    F_spring *= (spring.m1.p - spring.m2.p) / L
                    # Update F with appropriate sign
                    if spring.m1 == mass:
                        F += F_spring
                    else:
                        F -= F_spring



# %%

mu_s = 0.6 # Static coefficient of friction
mu_k = 0.7 # Kinetic coefficient of friction
# Calculate parallel and normal forces before the ground reaction force
            F_parallel = np.array([F[0], F[1], 0])
            F_normal = np.array([0, 0, F[2]]) 
            # GROUND COLLISION FORCE & FRICTION
            if mass.p[2] <= 0:
                # Normal reaction due to collision
                F_collision = np.array([0, 0, -kc * mass.p[2]])
                F += F_collision
                F_normal += F_collision  # Adjusting normal force with collision reaction
                # Static friction
                if np.linalg.norm(F_parallel) < np.linalg.norm(F_normal) * mu_s:
                    F -= F_parallel
                # Kinetic friction
                else:
                    kinetic_friction_magnitude = np.linalg.norm(F_N) * mu_k
                    F_friction = -kinetic_friction_magnitude * (F_P / np.linalg.norm(F_P))
                    F += F_friction
# %%
import numpy as np
# throwing cube with slight spin
#data = np.genfromtxt("Table_Body_points.txt", delimiter=',')
#print(data)

fbyf_4 = np.zeros((36,3))
fbyf_5 = np.zeros((36,3))

c=0
for i in range(6):
    for j in range(6):
        fbyf_4[c] = [i,j,3]
        fbyf_5[c] = [i,j,4]
        c+=1
        pass
    
    
fvf = np.vstack((fbyf_4,fbyf_5)).astype(int)

print('----------table top-------------')

leg1 = np.array([[0,0,0],
                [1,0,0],
                [0,1,0],
                [1,1,0],
                [0,0,1],
                [1,0,1],
                [0,1,1],
                [1,1,1],
                [0,0,2],
                [1,0,2],
                [0,1,2],
                [1,1,2],
                ])
#print(leg)
leg2 = leg1 + [4,0,0]
leg3 = leg1 + [0,4,0]
leg4 = leg1 + [4,4,0]

out = np.vstack((fvf,leg1,leg2,leg3,leg4)).astype(int)

print(out.size)
print(out*.1)
#%%
x,y,z = out[5]
print(x,y,z,'=', out[5])


#%%
file_path = "table_body.txt"

# Save the NumPy array to a text file
np.savetxt(file_path, out, fmt='%d', delimiter=',')
# %%
import numpy as np


points = np.genfromtxt("table_body.txt", delimiter=',')

rnd_ind = np.random.choice(points.shape[0], size=5, replace=False)
rnd_points = points[rnd_ind]
print(rnd_points)
for pt in rnd_points:
    print(pt)
out = [ (pt , np.random.choice([1,2,3,4])) for pt in rnd_points ]

print(out[0])
#%%
import numpy as np

# Create a 2D NumPy array (example data)
vertex = np.array([2, 3, 4])  # Example vertex
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

# Subtract the vertex from each row in the array
result = data - vertex

print("Result:")
print(result)

# %%

import matplotlib.pyplot as plt
import numpy as np

fig, ax1 = plt.subplots()
T = .07
y = np.random.uniform(0,.25,size = 50)
y_srt = np.sort(y)[::-1]
x = np.arange(len(y))
ax1.plot(x,y_srt, 'g-')  # 'g-' is for green solid line
ax1.set_xlabel('X data')
ax1.set_ylabel('Y1 data', color='g')
y_exp = np.exp(T * y_srt)-1

ax2 = ax1.twinx()
ax2.plot(x,y_exp, 'b-')  # 'b-' is for blue solid line
ax2.set_ylabel('Y2 data', color='b')




# %%
from Libraries import *
from Datastructures import*
import copy
body =  RandomBody()
body2 =  body.Body_deep_copy()
body2.genome[1] = None
print(body.genome[:3], '\n ---------------')
print(body2.genome[:3])
# %%
a = np.zeros(4)
print (np.exp(.05*(a + 1))-1)


# %%
import timeit

@jit(nopython=True) #non intensive but why not
def two_point_crossover_JIT(arr1, arr2, print_test = False):
    # Ensure arrays are of the same length
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must be of the same length")

    length = len(arr1)

    # Ensure array length is more than 3 to have non-neighboring indices
    if length < 4:
        raise ValueError("Arrays must have more than 3 elements for non-neighboring crossover points")

    # Select two random non-neighboring indices for crossover
    index1 = random.randint(0, length - 3)
    index2 = random.randint(index1 + 2, length - 1)
    
    # Create new child arrays
    new_arr1 = np.concatenate((arr1[:index1], arr2[index1:index2], arr1[index2:]))
    new_arr2 = np.concatenate((arr2[:index1], arr1[index1:index2], arr2[index2:]))

    if print_test:
        print("parent 1:", arr1)
        print("parent 2:", arr2)
        print('index1: ' , index1, '  index2: ',index2 )
        print("Child 1:" , new_arr1)
        print("Child 2:" , new_arr2)
    
    return new_arr1, new_arr2


def two_point_crossover(arr1, arr2, print_test = False):
    # Ensure arrays are of the same length
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must be of the same length")

    length = len(arr1)

    # Ensure array length is more than 3 to have non-neighboring indices
    if length < 4:
        raise ValueError("Arrays must have more than 3 elements for non-neighboring crossover points")

    # Select two random non-neighboring indices for crossover
    index1 = random.randint(0, length - 3)
    index2 = random.randint(index1 + 2, length - 1)
    
    # Create new child arrays
    new_arr1 = np.concatenate((arr1[:index1], arr2[index1:index2], arr1[index2:]))
    new_arr2 = np.concatenate((arr2[:index1], arr1[index1:index2], arr2[index2:]))

    if print_test:
        print("parent 1:", arr1)
        print("parent 2:", arr2)
        print('index1: ' , index1, '  index2: ',index2 )
        print("Child 1:" , new_arr1)
        print("Child 2:" , new_arr2)
    
    return new_arr1, new_arr2


a1 = np.random.uniform(size = 1000)
a2 = np.random.uniform(size = 1000)


execution_time1 = timeit.timeit("two_point_crossover(a1,a2)", number=15, globals=globals())
print(f"Execution time reg: {execution_time1} seconds")


execution_time2 = timeit.timeit("two_point_crossover_JIT(a1,a2)", number=15, globals=globals())
print(f"Execution time jit: {execution_time2} seconds")