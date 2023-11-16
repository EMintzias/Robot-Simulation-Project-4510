#%%
from Libraries import *
from Datastructures import *

#%%
class Simulate:
    def __init__(self, body):
        self.body = body
        self.Initial_pos = body.COM
        #GVLs
        self.b  = 0.999 # Dampening constant
        self.Kc = 100000  # Ground force constant
        self.G  = np.array([0, 0, -9.81])  # Gravity
        self.mu_s = 0.89 # Static friction
        self.mu_k = 0.70 # Kinetic friction
        self.dt = 0.00007  # Time-step
        self.T  = 0  # Global time variable
        self.omega = 2*np.pi
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
        mass_color = (0, 0, 0)
        spring_color = {1:(232/255, 177/255, 155/255), 2:(206/255, 222/255, 220/255), 3:(1, 0, 0), 4:(0, 0, 1)}  # Color springs for different types
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
        glBegin(GL_LINES)
        for spring in self.body.springs:
            glColor3fv(spring_color[spring.tissue_type])
            glVertex3fv(spring.m1.p)
            glVertex3fv(spring.m2.p)
        glEnd()
    
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
    
    def draw_ground(self):
        dark_grey = (0.4, 0.4, 0.4)  # Dark grey color
        light_grey = (0.6, 0.6, 0.6)  # Lighter grey color
        side_length = 1  # Length of the side of each square
        num_squares = 4  # Number of squares in each row and column
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
    
    ########################### RUN METHODS #######################################
    # TODO run faster!
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
                # Calculate spring force and actuator length based on time
                L = np.linalg.norm(spring.m1.p - spring.m2.p)
                Lo = spring.L0*(1+spring.b * np.sin(self.omega*self.T + spring.c))
                # Update F_spring in the vector direction from m2 to m1 (unit vect (p1-p1)/dist)
                F_spring = spring.k * (L - Lo) * (spring.m1.p - spring.m2.p) / L
                
                # Update F with appropriate sign
                if spring.m1 == mass:
                    F -= F_spring
                else:
                    F += F_spring
        # FRICTION FORCE
        if mass.p[2] <= 0:
            Fp = [F[0], F[1], 0]
            Fn = [0, 0, F[2]]
            if np.linalg.norm(Fp) < np.linalg.norm(Fn)*self.mu_s:
                F -= Fp
            else:
                F += Fp/np.linalg.norm(Fp)*(-1)*np.linalg.norm(Fn)*self.mu_k
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
    
    def evaluate(self, T = .05):
        dist = np.linalg.norm(self.Initial_pos - self.body.COM_update())
        return dist
    
    def print_update(self):
        out = f'Time = {round(self.T,2)}  |  '
        out+= f'Position  = {np.round(self.body.masses[72].p,2)}  |  '
        out+= f'Vel  = {np.round(self.body.masses[72].v,2)}  |  '
        print(out)
    
    def plot_frame(self): 
        pygame.init()
        #glutInit()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
        gluLookAt(-3.5, -3.5, 2.5, 0, 0, 0, 0, 0, 1)
        glClearColor(0.53, 0.81, 0.98, 1)
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return   

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.draw_ground()
        self.draw_cube()
        
        # Render the text in the top-right corner using GLUT
        text_string = f"Time: {self.T:.2f} seconds"
        self.render_text(0.6, 0.9, text_string)
        
        pygame.display.flip()
        #pygame.time.wait(10)      
    
    def run_simulation(self, Plot = False, Actuator_on = False, Verbose = False, max_T = 1): 

        if Plot:
            start_time = time.time()
            pygame.init()
            #glutInit()
            display = (800,600)
            pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
            gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
            gluLookAt(-2., -2., 1.5, 0, 0, 0, 0, 0, 1)
            glClearColor(0.53, 0.81, 0.98, 1)
            glDisable(GL_CULL_FACE)
            glEnable(GL_DEPTH_TEST)
               
            while True:
                #___________SIMULATION _________
                # Loop over all masses and update them, advance simulation one step
                #start_time = time.time()
                self.Body_Advance_step()
                #print(f"Running {len(self.body.springs)/(time.time() - start_time):.6f} springs/sec")

                # _________PLOTING_________
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                # _________RENDERING_________
                if self.global_step % 100 == 1:
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    self.draw_ground()
                    self.draw_cube()
                    # Render the text in the top-right corner using GLUT
                    text_string = f"Time: {self.T:.2f} seconds"
                    self.render_text(0.6, 0.9, text_string)
                    pygame.display.flip()
                    #pygame.time.wait(10)
                if self.T> max_T:
                    print(self.T)
                    print(f"Took {(time.time() - start_time):.6f} sec for {self.T} sec in sim")
                    break 
        
    
        else:
            # Run simulation without plotting
            start_time = time.time()
            while True: 
                self.Body_Advance_step()
                
                if Verbose and (self.global_step % self.sixty_Hz == 1):
                     self.print_update()
                
                if self.T> max_T:
                    print(f"Took {(time.time() - start_time):.6f} sec for {self.T} sec in sim")
                    break
        #desired output       
        return self.evaluate()
            



if __name__ == "__main__":
    BODY =  Custom_body_1(k_value=9000, p_0 = [0,0,0.])
    #BODY = CubeLattice(p_0 = [0,0,0.9])
    #print(len(BODY.springs))
    sim1 = Simulate(body = BODY)
    fitness = sim1.run_simulation(Plot = False, Verbose = True, max_T = 2)
    #cProfile.run('main(cubes)', 'profiling.out')
    print(fitness)
    print('done')

# %%
