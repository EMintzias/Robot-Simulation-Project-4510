#%%
from Libraries_cloud import *
from Datastructures_cloud import *
from Simulation_cloud import *

#%%
class EvolvingGait:
    def __init__(self, pop_size, Random_Search = False):
        self.pop_size = pop_size
        self.population = np.full(pop_size, dtype=object)
        self.fitnesses = np.zeros(pop_size, dtype=float64)

        self.random_population()
        self.update_pop_fitness()

        if Random_Search:
            self.random_search()

    # Populate with random bodies
    def random_population(self):
        for i in len(self.pop_size):
            self.population[i] = self.random_individual()
    
    def random_individual(self):
        return Custom_body_1()
        
    def update_pop_fitness(self):
        for i in tqdm(len(self.pop_size), desc='Evaluating:'):
            self.fitnesses[i] = Simulate(body=self.population[i]).run_simulation(Plot=False, max_T=0.01)

    def fitness_prop_selection(self):
        pass

    def mutate(self):
        pass

    def crossover(self):
        pass

    def random_search(self):
        return self.population


if __name__ == "__main__":
    
    population = EvolvingGait(pop_size = 60, Random_Search = True)
    
    filename = '{}_random_search.pkl'.format(time.time())
    with open(filename, 'wb') as file:
        pickle.dump(population, file)


