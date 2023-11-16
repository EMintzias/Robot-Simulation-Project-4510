#%%
from Libraries_cloud import *
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
    
    
    def run_simulation(self, Plot = False, Actuator_on = False, Verbose = False, max_T = 1): 


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
