#%%
from Project_Libries import *

# Functions to plot each object

vertices = (
    (1, 2, -1), (1, 4, -1),
    (-1, 4, -1), (-1, 2, -1),
    (1, 2, 1), (1, 4, 1),
    (-1, 2, 1), (-1, 4, 1)
)


# Cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Cube faces
faces = [
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7),
    (7, 6, 5, 4),  # Modified this face to be consistent with others
    (0, 3, 2, 1)  # Modified this face to be consistent with others
]



def draw_ground():
    glBegin(GL_QUADS)

    # Ground color
    ground_color = [0.5, 0.5, 0.5, 1.0]  # Grey
    # Set the material properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ground_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, ground_color)
    
    glVertex3fv((-40, -1.1, 40))
    glVertex3fv((40, -1.1, 40))
    glVertex3fv((40, -1.1, -40))
    glVertex3fv((-40, -1.1, -40))
    glEnd()

def draw_sphere(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # Sphere color
    sphere_color = [237/255, 123/255, 47/255, 1.0]  # Orange
    # Set the material properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, sphere_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, sphere_color)

    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()

def draw_cube(draw_faces = True, draw_edges=False):
    if draw_faces:
        # Draw faces
        glBegin(GL_QUADS)

        # Cube color
        cube_color = [3/255, 148/255, 252/255, 1.0]  # Blue
        # Set the material properties
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, cube_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, cube_color)

        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()
    
    if draw_edges:
        # Draw edges
        glLineWidth(2)  # Slightly thicker lines for edges
        glBegin(GL_LINES)
        edge_color = [3/255*0.2, 148/255*0.2, 252/255*0.2, 1.0]  # Dark Blue
        # Set the material properties
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, edge_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, edge_color)

        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    # Draw shadow cube
    glBegin(GL_QUADS)
    shadow_color = [0.2, 0.2, 0.2, 1.0]  # Dark grey
    # Set the material properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, shadow_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, shadow_color)

    for face in faces:
        for vertex in face:
            glVertex3f(vertices[vertex][0], 0, vertices[vertex][2])  # Set y-coordinate to 0
    glEnd()



def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(30, (display[0]/display[1]), 0.1, 200.0)
    glTranslatef(0.0, -2.0, -35)
    glRotatef(25, 1, 1, 0)
    glClearColor(0.53, 0.81, 0.98, 1)

    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)  # Enable lighting
    glEnable(GL_LIGHT0)  # Enable light source 0

    light_position = [20.0, 20.0, 20.0, 1.0]  # Positional light
    light_diffuse = [1, 1, 1, 1.0]  # Brighter white light
    light_ambient = [0.7, 0.7, 0.7, 1.0]  # Ambient light

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_ground()
        draw_cube()
        for vertex in vertices:
            draw_sphere(*vertex)
        pygame.display.flip()
        pygame.time.wait(10)

main()



# %%
from Project_Libries import *

# Vertices of the cube
vertices = (
    (1, 2, 2), (1, 4, 2),
    (-1, 4, 2), (-1, 2, 2),
    (1, 2, 4), (1, 4, 4),
    (-1, 2, 4), (-1, 4, 4)
)

# Cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Cube faces
faces = [
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7),
    (7, 6, 5, 4),
    (0, 3, 2, 1)
]

def draw_ground():
    glBegin(GL_QUADS)
    ground_color = [0.5, 0.5, 0.5, 1.0]  # Grey
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ground_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, ground_color)

    glVertex3fv((-40, -1.1, 0))
    glVertex3fv((40, -1.1, 0))
    glVertex3fv((40, -1.1, -40))
    glVertex3fv((-40, -1.1, -40))
    glEnd()

def draw_sphere(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    sphere_color = [237/255, 123/255, 47/255, 1.0]  # Orange
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, sphere_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, sphere_color)

    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()

def draw_cube():
    # Draw faces
    glBegin(GL_QUADS)
    cube_color = [3/255, 148/255, 252/255, 1.0]  # Blue
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, cube_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, cube_color)

    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Draw shadow cube
    glBegin(GL_QUADS)
    shadow_color = [0.2, 0.2, 0.2, 1.0]  # Dark grey
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, shadow_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, shadow_color)

    for face in faces:
        for vertex in face:
            glVertex3f(vertices[vertex][0], vertices[vertex][1], 0)  # Set z-coordinate to 0
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(30, (display[0]/display[1]), 0.1, 200.0)
    glTranslatef(0.0, 0.0, -35)
    #glRotatef(25, 1, 1, 0)
    glClearColor(0.53, 0.81, 0.98, 1)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)  # Enable lighting
    glEnable(GL_LIGHT0)  # Enable light source 0

    light_position = [20.0, 20.0, 20.0, 1.0]  # Positional light
    light_diffuse = [1, 1, 1, 1.0]  # Brighter white light
    light_ambient = [0.7, 0.7, 0.7, 1.0]  # Ambient light

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_ground()
        draw_cube()
        for vertex in vertices:
            draw_sphere(*vertex)
        pygame.display.flip()
        pygame.time.wait(10)

main()

# %%
