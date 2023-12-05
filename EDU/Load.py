from Libraries import *
from Datastructures import *
from Simulation_jit_v2 import *

with open('10_random_robots.pkl', 'rb') as file:
    data_loaded = pickle.load(file)

population = data_loaded['population']
fitness_raw = data_loaded['fitness_raw']
fitness_arr = data_loaded['fitness_arr']
fitness_ind = data_loaded['fitness_ind']

print(population)
print(fitness_raw)
print(fitness_arr)
print(fitness_ind)

f  = Simulate(population[np.argmax(fitness_raw)]).run_simulation(Plot=True, max_T=3)