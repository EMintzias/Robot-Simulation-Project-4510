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

# throwing cube with slight spin
for i, mass in enumerate(cube.masses):
            if i == 4 and T == 0:
                F = np.array([0,200,0.])
            else:
                # Initial force is 0
                F = np.zeros(3)