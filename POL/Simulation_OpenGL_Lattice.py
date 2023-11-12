#%%
from Libraries import *
from Datastructures import *

# Global Variables
g = np.array([0, 0, -9.81])  # Gravity
dt = 0.000075  # Time-step
T = 0  # Global time variable
global_step = 0
kc = 100000  # Ground force constant
b = 0.999 # Dampening constant

# Initialize cube
# cube = Cube(p_0= np.dot([0, 0, 1], 0.3), k_value=9000)

# Initialize cubes
#num_cubes = 1
#cubes = np.empty(num_cubes, dtype=object)

#for i in range(num_cubes):
#    x_rand = 0#np.random.uniform(-0.3, 0.3)
#    y_rand = 0#np.random.uniform(-0.3, 0.3)
#    z_rand = 0.9#np.random.uniform(0.2, 0.5)
#    cubes[i] = Cube(p_0= [x_rand, y_rand, z_rand], k_value=9000)

# Initialize lattice
lattice = CubeLattice(lattice_size=2, k_value=9000, p_0 = [0,0,0.9])

def draw_cube_faces(cube):
    base_color = (0/255, 120/255, 200/255)  # Blue color
    border_color = (0, 0, 0)  # Black color for the border
    border_width = 1  # Width of the border

    for i, face in enumerate(cube.faces):
        # Draw face
        glBegin(GL_QUADS)
        glColor3f(base_color[0], base_color[1], base_color[2])
        for mass in face:
            glVertex3fv(mass.p)
        glEnd()

        # Draw border
        glLineWidth(border_width)
        glColor3fv(border_color)
        glBegin(GL_LINES)
        for i in range(len(face)):
            glVertex3fv(face[i].p)
            glVertex3fv(face[(i + 1) % len(face)].p)  # Loop back to the start for the last line
        glEnd()

def draw_masses_and_springs(cube):
    mass_color = (1, 0, 0)  # Red color for masses
    spring_color = (0, 1, 0)  # Green color for springs
    mass_size = 5  # Size of the mass points
    spring_width = 1  # Width of the springs

    # Draw masses
    glPointSize(mass_size)
    glColor3fv(mass_color)
    glBegin(GL_POINTS)
    for mass in cube.masses:
        glVertex3fv(mass.p)
    glEnd()

    # Draw springs
    glLineWidth(spring_width)
    glColor3fv(spring_color)
    glBegin(GL_LINES)
    for spring in cube.springs:
        glVertex3fv(spring.m1.p)
        glVertex3fv(spring.m2.p)
    glEnd()

def draw_shadow(cube):
    shadow_color = (0.2, 0.2, 0.2)  # Dark gray color for shadow
    spring_shadow_width = 1  # Width of the spring shadows

    # Set the color and line width for the shadows
    glColor3fv(shadow_color)
    glLineWidth(spring_shadow_width)

    # Draw shadows of the springs
    glBegin(GL_LINES)
    for spring in cube.springs:
        # Project the mass positions onto the ground plane (z = 0)
        glVertex3f(spring.m1.p[0], spring.m1.p[1], -0.001)
        glVertex3f(spring.m2.p[0], spring.m2.p[1], -0.001)
    glEnd()


def draw_cube(cube):
    # Draw shadow first
    draw_shadow(cube)
    # Then draw the cube's faces
    #draw_cube_faces(cube)
    draw_masses_and_springs(cube)

def draw_ground():
    dark_grey = (0.4, 0.4, 0.4)  # Dark grey color
    light_grey = (0.6, 0.6, 0.6)  # Lighter grey color
    side_length = 1  # Length of the side of each square
    num_squares = 3  # Number of squares in each row and column

    glBegin(GL_QUADS)
    for i in range(num_squares):
        for j in range(num_squares):
            # Determine the color of the square
            if (i + j) % 2 == 0:
                glColor3fv(light_grey)
            else:
                glColor3fv(dark_grey)

            # Calculate the coordinates of the square
            x1 = i * side_length - 1.45
            y1 = j * side_length - 1.45
            x2 = x1 + side_length
            y2 = y1 + side_length

            # Draw the square
            glVertex3f(x1, y1, -0.005)
            glVertex3f(x2, y1, -0.005)
            glVertex3f(x2, y2, -0.005)
            glVertex3f(x1, y2, -0.005)
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

# TODO add friction force BEFORE vectorizing
# TODO vectorize to improve efficiency
# TODO re-write so only using numbers (no objects) so numba integration is trivial
def update_mass(mass):
    global T
    # Initial force is 0
    # GRAVITATIONAL FORCE
    # Update F
    F = mass.m * g
    # SPRING FORCE
    # Loop over all springs
    for spring in mass.springs:
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
    cube.masses = [update_mass(mass) for mass in cube.masses]
    return cube

def main(cube):
    global T, global_step

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    gluLookAt(-3.5, -3.5, 2.5, 0, 0, 0, 0, 0, 1)
    glClearColor(0.53, 0.81, 0.98, 1)
    glDisable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # BREATHING CUBE
        if False:
            for cube in cubes:
                for spring in cube.springs:
                    spring.L0 += 0.00005*np.sin(global_step*0.001)

        start_time = time.time()
        
        # Loop over all masses
        update_cube(cube)
        
        T += dt
        global_step += 1

        #print(f"Each update loop takes {time.time() - start_time:.6f} seconds")

        if global_step%20 == 1:

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            draw_ground()
            draw_cube(cube)
            # Convert the time to a string
            text_string = f"Time: {T:.2f} seconds"
            # Render the text in the top-right corner using GLUT
            render_text(0.6, 0.9, text_string)
            pygame.display.flip()
            #pygame.time.wait(10)

if __name__ == "__main__":
    main(lattice)
    #cProfile.run('main(cubes)', 'profiling.out')

