#%%
from Libraries import *
from Datastructures import *
import pstats
from my_dtypes import mass_dtype, spring_dtype
#%%

#GLOBAL MASS UPDATE FUNCTION
@jit(nopython=True)
def mass_update_jit(old_masses_arr,springs_arr, T,  
                    dt = 0.00007,
                    G = np.array([0, 0, -9.81]), # Gravity
                    b  = 0.999,         # Dampening constant
                    Kc = 100000,        # Ground force constant
                    mu_s = 0.89,        # Static friction
                    mu_k = 0.70,        # Kinetic friction
                    omega = 3*2*np.pi,                         
                        ):

    #update simulation
    new_masses = old_masses_arr.copy()

    for mass_ind,mass in enumerate(new_masses): 
        
        # Initial force is 0
        # GRAVITATIONAL FORCE
        # Update F

        F = mass['m'] * G
        
        # SPRING FORCE
        # Loop over all springs
        for s_ind,spring in enumerate(springs_arr):
            # If spring connected to that mass
            if spring['m1_ind']  == mass_ind or spring['m2_ind'] == mass_ind:
                # Calculate spring force and actuator length based on time
                M1,M2 = old_masses_arr[spring['m1_ind']], old_masses_arr[spring['m2_ind']] 
                
                L = np.linalg.norm(M1['p'] - M2['p'])
                Lo = spring['L0']*(1+spring['b'] * np.sin(omega* T + spring['c']))
                # Update F_spring in the vector direction from m2 to m1 (unit vect (p1-p1)/dist)
                F_spring = spring['k'] * (L - Lo) * (M1['p'] - M2['p']) / L
                
                # Update F with appropriate sign
                if spring['m1_ind']  == mass_ind:
                    F -= F_spring
                else:
                    F += F_spring
        
        # FRICTION FORCE
        if mass['p'][2] <= 0:
            Fp = np.array([F[0], F[1], 0])
            Fn = np.array([0, 0, F[2]])
            if np.linalg.norm(Fp) < np.linalg.norm(Fn)* mu_s:
                F -= Fp
            else:
                F += Fp/np.linalg.norm(Fp)*(-1)*np.linalg.norm(Fn)* mu_k
        
        # GROUND COLLISION FORCE
        # Ground collision check and response
        if mass['p'][2] < 0:
            F += np.array([0, 0, - Kc * mass['p'][2]])
        
        # UPDATE ACCELERATION
        mass['a'] = F / mass['m']
        # UPDATE VELOCITY
        mass['v'] += mass['a'] *  dt
        mass['v'] *=  b # dampening
        # UPDATE POSITION
        mass['p'] += mass['v'] *  dt
        
        new_masses[mass_ind] = mass #i think this is redundant since it happened above?
        
    return new_masses


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
        self.masses_arr, self.springs_arr = self.get_dtype_arrays() #JIT Dtypes redundant rewriting for class clarity.
        
    #_______________________________________
    
    
    ############################
    ####  PLOTTING METHODS #####
    ############################
    
    #______________________________________________________________________
    
    
    ########################### 
    ####### RUN METHODS #######
    ###########################
     
    def get_dtype_arrays(self):
        masses_arr = np.empty(len(self.body.masses), dtype=mass_dtype)

        for i,mass in enumerate(self.body.masses):
            masses_arr[i]['m'] = mass.m
            masses_arr[i]['p'] = mass.p
            masses_arr[i]['v'] = mass.v
            masses_arr[i]['a'] = mass.a

        springs_arr = np.empty(len(self.body.springs), dtype=spring_dtype)
        ind_arr = np.arange(len(self.body.masses))
        
        for i,spring  in enumerate(self.body.springs):
            springs_arr[i]['k'] = spring.k
            springs_arr[i]['b'] = spring.b
            springs_arr[i]['c'] = spring.c
            springs_arr[i]['L0'] = spring.L0
            springs_arr[i]['m1_ind'] = ind_arr[[spring.m1 == mass for mass in self.body.masses]][0]
            springs_arr[i]['m2_ind'] = ind_arr[[spring.m2 == mass for mass in self.body.masses]][0]
            springs_arr[i]['center'] = spring.center
            springs_arr[i]['tissue_type'] = spring.tissue_type
        
        self.masses_arr, self.springs_arr = masses_arr, springs_arr
        
        return masses_arr, springs_arr
    
    def update_mass_obj(self,masses_arr = None):
        
        if not masses_arr: 
            masses_arr  = self.masses_arr
        
        for i,mass in enumerate(self.body.masses):
            mass.m = masses_arr[i]['m']
            mass.p = masses_arr[i]['p']
            mass.v = masses_arr[i]['v']
            mass.a = masses_arr[i]['a']

    
    def Body_Advance_step_jit(self):
        self.masses_arr = mass_update_jit(self.masses_arr.copy(),self.springs_arr, self.T)
        
        #update simulation
        self.T+=self.dt
        self.global_step +=1
        pass
    
    def evaluate(self, T = .05):
        dist = np.linalg.norm(self.Initial_pos - self.body.COM_update())
        return dist
    
    def print_update(self):
        out = f'Time = {round(self.T,2)}  |  '
        out+= f'Position  = {np.round(self.body.masses[0].p,2)}  |  '
        out+= f'Vel  = {np.round(self.body.masses[0].v,2)}  |  '
        print(out)
    
    def run_simulation(self, Plot = False, Actuator_on = False, Verbose = False, max_T = 1): 
        start_time = time.time()
        if Plot:
               
            while True:
                #___________SIMULATION _________
                # Loop over all masses and update them, advance simulation one step
                #start_time = time.time()
                
                self.Body_Advance_step_jit()
                    
                # ____ END CASE____ 
                if self.T> max_T:
                    self.update_mass_obj() #JIT: update mass obj to the array iterated
                    break 
        
    
        else:
            # Run simulation without plotting
            start_time = time.time()
            while True: 
                self.Body_Advance_step_jit()
                
                if Verbose and (self.global_step % self.sixty_Hz == 1):
                     self.update_mass_obj() #JIT: update mass obj to the array iterated
                     self.print_update()
                
                if self.T> max_T:
                    self.update_mass_obj() #JIT: update mass obj to the array iterated
                    break
        
        
        #END OF SIMULATION: desired output 
        #print(f"Took {(time.time() - start_time):.6f} sec for {self.T} sec in sim")           
        self.body.fitness = self.evaluate()
        return self.body.fitness 





def start_profiler():
    profiler = cProfile.Profile()
    profiler.enable()
    return profiler

def end_profiler(profiler, Dump_stats = True, Verbose = True):
    profiler.disable()
    
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    
    if Verbose:     stats.print_stats()
    if Dump_stats:  stats.dump_stats('profile_stats.prof')
    


if __name__ == "__main__":
    #NEW_BODY = CubeLattice(lattice_size=2, p_0=np.array([0,0,.5]))
    NEW_BODY = RandomBody(only_bounce=False)
    #print(NEW_BODY.genome)
    sim1 = Simulate(body = NEW_BODY)
    #profiler = start_profiler()
    fitness = sim1.run_simulation(Plot = True, Verbose = True, max_T = 3)
    #end_profiler(profiler)
    print(NEW_BODY.masses)

    
    print('done')