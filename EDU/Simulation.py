#%%
from Libraries import *
from Datastructures import *

#%%
class Simulate:
    def __init__(self, body) -> None:
        self.body = body
        self.Initial_pos = body.COM
        
        #GVLs
        self.b  = 0.999 # Dampening constant
        self.Kc = 100000  # Ground force constant
        self.G  = np.array([0, 0, -9.81])  # Gravity
        self.dt = 0.000075  # Time-step
        self.T  = 0  # Global time variable
        self.global_step = 0
        self.sixty_Hz = int(0.01666 / self.dt) # dynamic plotting for 60 FPS 
        self.four_Hz = int(.25 / self.dt)
    
    #######################  PLOTTING METHODS ######################################
    
    
    def draw_cube_faces(self):
        base_color = (0/255, 120/255, 200/255)  # Blue color
        border_color = (0, 0, 0)  # Black color for the border
        border_width = 1  # Width of the border

        for i, face in enumerate(self.body.faces):
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
    
    def draw_masses_and_springs(self):
        mass_color = (1, 0, 0)  # Red color for masses
        spring_color = (0, 1, 0)  # Green color for springs
        mass_size = 5  # Size of the mass points
        spring_width = 1  # Width of the springs

        # Draw masses
        glPointSize(mass_size)
        glColor3fv(mass_color)
        glBegin(GL_POINTS)
        for mass in self.body.masses:
            glVertex3fv(mass.p)
        glEnd()

        # Draw springs
        glLineWidth(spring_width)
        glColor3fv(spring_color)
        glBegin(GL_LINES)
        for spring in self.body.springs:
            glVertex3fv(spring.m1.p)
            glVertex3fv(spring.m2.p)
        glEnd()
        
        pass
    
    def draw_shadow(self):
        shadow_color = (0.2, 0.2, 0.2)  # Dark gray color for shadow
        spring_shadow_width = 1  # Width of the spring shadows

        # Set the color and line width for the shadows
        glColor3fv(shadow_color)
        glLineWidth(spring_shadow_width)

        # Draw shadows of the springs
        glBegin(GL_LINES)
        for spring in self.body.springs:
            # Project the mass positions onto the ground plane (z = 0)
            glVertex3f(spring.m1.p[0], spring.m1.p[1], -0.001)
            glVertex3f(spring.m2.p[0], spring.m2.p[1], -0.001)
        glEnd()
        
        pass
    
    def draw_ground(self):
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
    
    def render_text(self, x, y, text):
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
        
    def draw_cube(self):
        # Draw shadow first
        self.draw_shadow()
        # Then draw the cube's faces
        #draw_cube_faces(self.body)
        self.draw_masses_and_springs()
        
        pass
    
    ########################### RUN METHODS #######################################
    def update_mass(self, mass):
        # Initial force is 0
        # GRAVITATIONAL FORCE
        # Update F
        F = mass.m * self.G
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
            F += np.array([0, 0, -self.Kc * mass.p[2]])
        # UPDATE ACCELERATION
        mass.a = F / mass.m
        # UPDATE VELOCITY
        mass.v += mass.a * self.dt
        mass.v *= self.b # dampening
        # UPDATE POSITION
        mass.p += mass.v * self.dt
        return mass
    
    def Body_Advance_step(self):
        #Update masses
        self.body.masses = [self.update_mass(mass) for mass in self.body.masses]
        
        #update simulation
        self.T+=self.dt
        self.global_step +=1
        pass
    
    def evaluate(self):
        COM = self.body.COM_update()
        

        VC
    
    def print_update(self):
        out = f'Time = {round(self.T,2)}  |  '
        out+= f'Position  = {np.round(self.body.masses[0].p,2)}  |  '
        out+= f'Vel  = {np.round(self.body.masses[0].v,2)}  |  '
        
        print(out)
               
        pass
    
    def run_simulation(self, Plot = False, Actuator_on = False, Verbose = False): 

        if Plot:
            pygame.init()
            #glutInit()
            display = (800,600)
            pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
            gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
            gluLookAt(-3.5, -3.5, 2.5, 0, 0, 0, 0, 0, 1)
            glClearColor(0.53, 0.81, 0.98, 1)
            glDisable(GL_CULL_FACE)
            glEnable(GL_DEPTH_TEST)
               
            while True:
                #___________SIMULATION _________
                # Loop over all masses and update them, advance simulation one step
                self.Body_Advance_step()

                #print(f"Each update loop takes {time.time() - start_time:.6f} seconds")

                
                
                # _________PLOTING_________
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                # BREATHING CUBE
                #TODO
                if Actuator_on:
                    for cube in cubes:
                        for spring in cube.springs:
                            spring.L0 += 0.00005*np.sin(self.global_step*0.001)

                start_time = time.time()
                
                
            
                if self.global_step % 200 == 1:

                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    self.draw_ground()
                    self.draw_cube()
                    
                    # Render the text in the top-right corner using GLUT
                    text_string = f"Time: {self.T:.2f} seconds"
                    #self.render_text(0.6, 0.9, text_string)
                    
                    pygame.display.flip()
                    #pygame.time.wait(10)      
                    
                if self.T> 10:
                    print(self.T)
                    break 
        
    
        else:
            # Run simulation without plotting
            
            while True: 
                self.Body_Advance_step()
                
                if Verbose and (self.global_step % self.four_Hz == 1):
                     self.print_update()
                    
                
                
                if self.T> 10:
                    break
    
    
        #desired output       
        return None
            



if __name__ == "__main__":
    lattice = CubeLattice(lattice_size=1, k_value=9000, p_0 = [0,0,0.9])
    sim1 = Simulate(body = lattice)
    sim1.run_simulation(Plot = True)
    #cProfile.run('main(cubes)', 'profiling.out')
    print('done')
