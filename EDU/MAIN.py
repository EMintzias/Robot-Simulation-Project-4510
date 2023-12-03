#%%
from Libraries import *
from Datastructures_cloud import *
from Simulation_cloud import *

#%%
class EvolvingGait:
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.population = np.empty(pop_size, dtype=object)
        self.fitnesses = np.zeros(pop_size, dtype=float)

        self.random_population()
        self.update_pop_fitness()

    # Populate with random bodies
    def random_population(self):
        for i in range(self.pop_size):
            self.population[i] = self.random_individual()
    
    def random_individual(self):
        return Custom_body_1()
        
    def update_pop_fitness(self):
        for i in tqdm(range(self.pop_size), desc='Evaluating:'):
            self.fitnesses[i] = Simulate(body=self.population[i]).run_simulation(Plot=False, max_T=2)

    def fitness_prop_selection(self):
        pass

    def mutate(self):
        pass

    def crossover(self):
        pass

    def results(self):
        return [self.population, self.fitnesses]


if __name__ == "__main__":
    
    t = EvolvingGait(pop_size = 12)
    
    pop_n_fit = t.results()

    filename = '{}_random_search.pkl'.format(time.time())
    with open(filename, 'wb') as file:
        pickle.dump(pop_n_fit, file)


