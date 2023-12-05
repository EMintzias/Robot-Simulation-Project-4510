#%%
from Libraries import *
from Datastructures import *
import pstats
from my_dtypes import mass_dtype, spring_dtype
from Simulation_jit_v2 import *
#%%

if __name__ == "__main__":
    with open('my_object.pkl', 'rb') as file:
        my_object = pickle.load(file)
    #my_object = RandomBody(only_bounce=False)
    my_object.reset_body_position()
    sim1 = Simulate(body = my_object)
    fitness = sim1.run_simulation(Plot = True, Verbose = True, max_T = 1)
    #with open('my_object.pkl', 'wb') as file:
    #    pickle.dump(my_object, file)