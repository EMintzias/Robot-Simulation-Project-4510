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
b = 0.999 # Dampening constant

# Initialize cube
cube = Cube(k_value=5000)

def draw_shadow(cube):
    glColor3f(0.3, 0.3, 0.3)  # Dark gray color for shadow
    glBegin(GL_LINES)
    for spring in cube.springs:
        start_point = list(spring.m1.p)
        end_point = list(spring.m2.p)
        start_point[2] = 0  # Set z-coordinate to 0
        end_point[2] = 0    # Set z-coordinate to 0
        glVertex3fv(start_point)
        glVertex3fv(end_point)
    glEnd()

def draw_cube(cube):
    glLineWidth(1)
    draw_shadow(cube)
    glBegin(GL_LINES)
    glColor3f(3/255*0.5, 148/255*0.5, 252/255*0.5)  # Blue color for springs
    for spring in cube.springs:
        start_point = spring.m1.p
        end_point = spring.m2.p
        glVertex3fv(start_point)
        glVertex3fv(end_point)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)  # Red color for masses
    for mass in cube.masses:
        glVertex3fv(mass.p)
    glEnd()

def draw_ground():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-0.3, -0.3, 0)
    glVertex3f(0.5, -0.3, 0)
    glVertex3f(0.5, 0.5, 0)
    glVertex3f(-0.3, 0.5, 0)
    glEnd()

def main(cube):
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    gluLookAt(-0.7, -0.7, 0.7, 0, 0, 0, 0, 0, 1)
    glClearColor(0.53, 0.81, 0.98, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
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
                F += np.array([0, 0, -kc * mass.p[2]])
            # UPDATE ACCELERATION
            mass.a = F / mass.m
            # UPDATE VELOCITY
            mass.v += mass.a * dt
            mass.v *= b
            # UPDATE POSITION
            mass.p += mass.v * dt
        T += dt
        global_step += 1
        total_elapsed_time += time.time() - start_time
        #print(f"Each update loop takes on avg {total_elapsed_time/global_step:.6f} seconds")

        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_ground()
        draw_cube(cube)
        pygame.display.flip()
        pygame.time.wait(10)

main(cube)
