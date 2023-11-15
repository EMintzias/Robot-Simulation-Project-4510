#%%
from Libraries import *
from Datastructures import Cube


# Global Variables
g = np.array([0, 0, -9.81])  # Gravity
dt = 0.0001  # Time-step
T = 0  # Global time variable
global_step = 0
total_elapsed_time = 0
kc = 100000  # Ground force constant

# Initialize cube
cube = Cube(k_value=5000)
#%%
# Helper function to plot the cube using matplotlib
def plot_cube(cube, ax):
    # Clear the current axes
    ax.cla()

    # Plotting the ground plane
    xx, yy = np.meshgrid(np.linspace(-0.15, 0.25, 100), np.linspace(-0.15, 0.25, 100))
    zz = np.dot(np.ones_like(xx),-0.1)
    ax.plot_surface(xx, yy, zz, color=(40/255, 40/255, 40/255), alpha=0.1)  # Dark grey color
    
    ax.set_axisbelow(True)

    for spring in cube.springs:
        start_point = spring.m1.p
        end_point = spring.m2.p
        ax.plot([start_point[0], end_point[0]],
                [start_point[1], end_point[1]],
                [-0.1, -0.1], 'grey')
        ax.plot([start_point[0], end_point[0]],
                [start_point[1], end_point[1]],
                [start_point[2], end_point[2]], 'b-')
        
    
    for mass in cube.masses:
        ax.scatter(*mass.p, s=50, c='r', marker='o')

    ax.set_xlim(-0.15, 0.25)
    ax.set_ylim(-0.15, 0.25)
    ax.set_zlim(-0.1, 0.3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#plot_cube(cube, ax)

#%%
def simulate(cube):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def update(frame, cube, ax):
        global T, global_step, total_elapsed_time
        # Loop over all masses
        start_time = time.time()
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
                print(mass.p[2])
                F += np.array([0, 0, -kc * mass.p[2]])
            # UPDATE ACCELERATION
            mass.a = F / mass.m
            # UPDATE VELOCITY
            mass.v += mass.a * dt
            # UPDATE POSITION
            mass.p += mass.v * dt
        T += dt
        global_step += 1
        total_elapsed_time += time.time() - start_time
        print(f"Each update loop takes on avg {total_elapsed_time/global_step:.6f} seconds")

        # After every 100 simulation steps, plot the cube
        if global_step % 1 == 0:
            plot_cube(cube, ax)
            return ax,

    def infinite_gen():
        while True:
            yield None

    ani = FuncAnimation(fig, update, frames=infinite_gen(), fargs=[cube, ax], interval=0, blit=False, cache_frame_data=False)

    plt.show()


simulate(cube)  # Simulate for 10 seconds



# %%
