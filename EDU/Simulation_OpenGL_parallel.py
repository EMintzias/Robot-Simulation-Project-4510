#%%
from Libraries import *
from Datastructures import Cube

# Number of cores 
num_cores = 2 #os.cpu_count() #8

# Global Variables
g = np.array([0, 0, -9.81])  # Gravity
dt = 0.0001  # Time-step
T = 0  # Global time variable
global_step = 0
total_elapsed_time = 0
kc = 100000  # Ground force constant
b = 0.999 # Dampening constant

# Initialize cubes
num_cubes = 4
cubes = np.empty(num_cubes, dtype=object)

for i in range(num_cubes):
    x_rand = np.random.uniform(-0.3, 0.3)
    y_rand = np.random.uniform(-0.3, 0.3)
    z_rand = np.random.uniform(0.1, 0.3)
    cubes[i] = Cube(p_0= [x_rand, y_rand, z_rand], k_value=9000)

#%%
def draw_cube_faces(cube):
    base_color = (3/255, 148/255, 252/255)  # Blue color
    glBegin(GL_QUADS)
    for i, face in enumerate(cube.faces):
        color_factor = 0.4 + (i + 1)*0.05  # '+1' to avoid zero multiplier for the first face
        glColor3f(base_color[0]*color_factor, base_color[1]*color_factor, base_color[2]*color_factor)
        for mass in face:
            glVertex3fv(mass.p)
    glEnd()

def draw_shadow(cube):
    glColor3f(0.3, 0.3, 0.3)  # Dark gray color for shadow
    glBegin(GL_QUADS)
    for i, face in enumerate(cube.faces):
        for mass in face:
            glVertex3fv([mass.p[0], mass.p[1], 0.00001])
    glEnd()

def draw_cube(cube):
    # Draw shadow first
    draw_shadow(cube)
    # Then draw the cube's faces
    draw_cube_faces(cube)

def draw_ground():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-0.3, -0.3, 0)
    glVertex3f(0.5, -0.3, 0)
    glVertex3f(0.5, 0.5, 0)
    glVertex3f(-0.3, 0.5, 0)
    glEnd()

def render_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0, 0, 0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def update_mass(cube, mass):
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
    return mass


def update_cube(cube):
    cube.masses = [update_mass(cube, mass) for mass in cube.masses]
    return cube


def main():

    global cubes
    
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    gluLookAt(-0.7, -0.7, 0.7, 0, 0, 0, 0, 0, 1)
    glClearColor(0.53, 0.81, 0.98, 1)
    glDisable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    # Initialize ThreadPool once
    executor = ThreadPoolExecutor(max_workers=num_cores)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        global T, global_step, total_elapsed_time
        
        # BREATHING CUBE
        if False:
            for spring in cube.springs:
                spring.L0 += 0.00005*np.sin(global_step*0.001)

        start_time = time.time()

        # Loop over all cubes and update masses in parallel
        list(executor.map(update_cube, cubes))

        
        T += dt
        global_step += 1

        total_elapsed_time = time.time() - start_time
        print(f"Each update loop takes {total_elapsed_time:.6f} seconds")

        if global_step%20 == 1:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            draw_ground()
            for cube in cubes:
                draw_cube(cube)
            # Convert the time to a string
            text_string = f"Time: {T:.2f} seconds"
            # Render the text in the top-right corner using GLUT
            render_text(0.6, 0.9, text_string)
            pygame.display.flip()
            #pygame.time.wait(10)

if __name__ == "__main__":
    #main()
    cProfile.run('main()', 'profiling_parallel.out')
