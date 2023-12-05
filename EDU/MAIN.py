#%%
from Libraries import *
from Datastructures import *
from Simulation_jit_v2 import *

#%%
#GLOBAL FUNCTIONS: 

def two_point_crossover(arr1, arr2, print_test = False):
    # Ensure arrays are of the same length
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must be of the same length")

    length = len(arr1)

    # Ensure array length is more than 3 to have non-neighboring indices
    if length < 4:
        raise ValueError("Arrays must have more than 3 elements for non-neighboring crossover points")

    # Select two random non-neighboring indices for crossover
    index1 = random.randint(0, length - 3)
    index2 = random.randint(index1 + 2, length - 1)
    
    # Create new child arrays
    new_arr1 = np.concatenate((arr1[:index1], arr2[index1:index2], arr1[index2:]))
    new_arr2 = np.concatenate((arr2[:index1], arr1[index1:index2], arr2[index2:]))

    if print_test:
        print("parent 1:", arr1)
        print("parent 2:", arr2)
        print('index1: ' , index1, '  index2: ',index2 )
        print("Child 1:" , new_arr1)
        print("Child 2:" , new_arr2)
    
    return new_arr1, new_arr2



#########################################
######## ROBOT Evolution ################
#########################################


class Robot_Population:
    def __init__(self, pop_size, simulation_time = 1.5):
        self.pop_size = pop_size
        self.original_body = RandomBody()
        self.population = np.empty(pop_size, dtype=object)
        self.fitness_raw = np.zeros(pop_size, dtype=float)  # Raw fitnesses
        self.fitness_arr = np.zeros(pop_size, dtype=float)  # fitnesses with selection pressure
        self.fitness_ind = np.zeros(pop_size, dtype=float) #points to the best robots
        self.sim_time = simulation_time
        self.evaluations = 0
        self.best_fitness = 1e-9
        self.generate_random_population()
        self.update_pop_fitness() 
        

    
    
    # Populate with random genomes for one body. 
    def generate_random_population(self):
        for i in tqdm(range(self.pop_size),desc='Generating Population'):
            deep_copy = self.original_body.Body_deep_copy()
            deep_copy.randomize_genome(Size = 8) 
            self.population[i] = deep_copy 

        pass
        
    #TODO confirm this is only thing we need to check after a simulation
    def reset_body_position(self,Body: RandomBody): 
        Body.masses = self.original_body.masses
    
    def evaluate_robot(self,Body: RandomBody): 
        fitness_raw  = Simulate(Body).run_simulation(max_T=self.sim_time)
        self.evaluations +=1
        #TODO idunno was up with the reset after it is done. 
        self.Body.reset_body_position() #bring the body back to a starting position for a new simualtion
        return fitness_raw
        
    def update_pop_fitness(self, T = .05):
        for i in tqdm(range(self.pop_size), desc='Simulating Population'):
            self.fitness_raw[i] = self.evaluate_robot(Body=self.population[i])
        self.fitness_arr = np.exp(T*(self.fitness_raw + 1e-9)) -1
        self.fitness_ind = np.argsort(self.fitness_arr)[::-1]
        self.best_fitness = self.fitness_arr[self.fitness_ind[0]]
        return 

    
    # SELECTION
    def fitness_prop_selection(self, N= 2):
        total_fitness    = np.sum(self.fitness_arr)
        self.fitness_ind = np.argsort(self.fitness_arr)[::-1]
        
        P1_ind, P2_ind = None, None
        Rand_1 = np.random.uniform(0, total_fitness/N)
        Rand_2 = Rand_1 + total_fitness/N
        
        accumulated_fitness = 0
        for ind in self.fitness_ind:
            accumulated_fitness += self.fitness_arr[ind]
            if accumulated_fitness >= Rand_1:
                if not P1_ind:
                    P1_ind = ind
                    continue

                if accumulated_fitness >= Rand_2:
                    P2_ind = ind
                    break

        return P1_ind, P2_ind
    
    #CROSSOVER  
    def crossover(self,P1: RandomBody,P2: RandomBody): 
        C1 = P1.Body_deep_copy()
        C2 = P2.Body_deep_copy()
        C1.genome, C2.genome = two_point_crossover(C1.genome, C2.genome)
        
        return C1,C2
    
    #MUTATION
    def Mutate(self,C1: RandomBody,C2: RandomBody):
        C1.Mutate_genome(mutation_size = .10,
                         Tissue_mutation = True, Tissue_prob = .25)
        C2.Mutate_genome(mutation_size = .10,
                         Tissue_mutation = True, Tissue_prob = .25)
        pass
    
    #GA MAIN
    def Crossover_Mutate_Replace(self, P1_ind, P2_ind):
        P1, P2 = self.population[P1_ind], self.population[P2_ind]
        
        #Crossover 
        C1, C2 = self.crossover(P1,P2)
        
        #mutation
        self.Mutate(C1, C2)
        
        
        #simulate the new children
        c1_fit = self.evaluate_robot(Body=C1)
        c2_fit = self.evaluate_robot(Body=C2)
        #Simulate(body=C1).run_simulation(max_T=self.sim_time)
        #Simulate(body=C2).run_simulation(max_T=self.sim_time)
        # NAIVE REPLACEMENT: Select the best two between parent and new children
        # TODO Implement discrete diversity maintenance here
        candidates = np.array([P1, P2, C1, C2])
        C_fitness = np.array([P1.fitness,
                              P2.fitness,
                              C1.fitness,
                              C2.fitness])
        best = np.argsort(C_fitness)[::-1]

        # overwrite the two parent indecies with the best population and their fitnesses
        self.population[P1_ind] = candidates[best[0]]
        self.fitness_arr[P1_ind] = C_fitness[best[0]]
        self.population[P2_ind] = candidates[best[1]]
        self.fitness_arr[P2_ind] = C_fitness[best[1]]

        self.fitness_ind = np.argsort(self.fitness_arr)[::-1]
        self.best_fitness = self.fitness_arr[self.fitness_ind[0]]

        return None
  
    #PRINT
    def results(self):
        return [self.population, self.fitness_raw]
    
    # MAIN LOOP
    def Run(self, max_simulations = 15, Update_freq = 1e7):
        
        with tqdm(total=max_simulations, unit="evaluation") as pbar:
            past_evals = 0

            while max_simulations > self.evaluations :
                # TODO update fitness based on some T criteria
                P1_ind, P2_ind = self.fitness_prop_selection()
                self.Crossover_Mutate_Replace(P1_ind, P2_ind)
                # the above replaces in population and writes to the fitness array so we have to resor
                
                pbar.update(self.evaluations - past_evals)
                pbar.set_description(f'Best distance: {self.best_fitness:.6f}')
                past_evals = self.evaluations

        return None
    

def Main():
    pop1 = Robot_Population(pop_size=4,
                            simulation_time= .25)
    pop1.Run()
    pass
    '''
    filename = '{}_random_search.pkl'.format(time.time())
    with open(filename, 'wb') as file:
        pickle.dump(pop_n_fit, file)
    '''
#%%
if __name__ == "__main__":
    Main()


#%%

pop1 = Robot_Population(pop_size=2,
                            simulation_time= .05)
#%%

pop1.Run(max_simulations=30)

#%%
print(pop1.original_body.masses[1])
print(pop1.population[1].masses[1])
pop1.reset_body_position(pop1.population[1])
print(pop1.population[1].masses[1])
    