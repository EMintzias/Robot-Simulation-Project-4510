# %%
# Libraries should be defined in each module the below call is a catch all in case some are missed.
#I think this i show you do it? if no paste them here
from EDU import Libraries, Datastructures, Simulation
from Libraries import *
from Datastructures import *
from Simulation import *

# SOME MODULES:


# %%

# we break this into population and EP classes since we can do ALPS trivialy in that way!
class Population: 
    def __init__(self,pop_size = 10) -> None:
        self.bodies = []
        self.T_max = 10 #sec
        self.
        
        
    
    def crossover(self):
        
        #TODO simple two point corssover should be good. selection might be tricky
        pass
    def mutation(self):
        #TODO suggest moving one or more of the centroids to a newarby random mass! (check for edge case of centroid collision)
        # this rutine should probably live in the body class 
        pass
    
    def evolve(self):
        #TODO:
        #let them flop around and evaluate their performance after the simulation
        # NOTE at the moment simulation has atribute 'distance_from_start' we can use this to create a fitness
        #recall exponential fitness from HW2, we can also just maximize distance. Depending on selection choice. 
         
        pass


class Robot_evolution_GA:
    def __init__(self,pop_size = 10) -> None:
        self.T = T
        self.evaluations = 0
        self.populations = []
        pass
        
        
    def evolve_populations(self):
        #TODO calls population evolution, their crossover etc
        pass
    
    def ALPS(self):
        #TODO governs population shifts given performance after some evolution threshold. 
        pass
    def run(self):
        '''
        MAIN FUNCTION: 
        
        in parallel (each core driving one) evolve each popoulation X generation
        
        pause and upgrade the top ten % of each to the next higher tier, 
        for the top take the bottom 10 and put them in the first tier
        
        
        '''
        
        
        pass
        
    
    
    
    
    
    
    some_cube = Cube(P_o=np.array([1, 2, 3]),
                     floor_size=3)
    some_cube.Plot()
    print(type(some_cube))


if __name__ == "__main__":
    # Test()
    main()

# %%
