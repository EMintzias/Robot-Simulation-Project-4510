#%%
import numpy as np
from Datastructures import Cube

#%%
# MASS DTYPE
mass_dtype = np.dtype([
            ('m', np.float64),
            ('p', np.float64, (3,)),
            ('v', np.float64, (3,)),
            ('a', np.float64, (3,)),
            ('springs', np.int32, (26,)),
            ('springs_i', np.int32, (26,)),
        ])

# SPRING DTYPE
spring_dtype = np.dtype([
            ('m1_ind', np.int32),
            ('m2_ind', np.int32),
            ('L0', np.float64),
            ('center', np.float64, (3,)),
            ('tissue_type', np.int32),
            ('k', np.float64),
            ('b', np.float64),
            ('c', np.float64)
        ])

#%%
if __name__ == "__main__":
    
    body = Cube()
    masses_nparr = np.empty(len(body.masses), dtype=mass_dtype)

    for i,mass in enumerate(body.masses):
        masses_nparr[i]['m'] = mass.m
        masses_nparr[i]['p'] = mass.p
        masses_nparr[i]['v'] = mass.v
        masses_nparr[i]['a'] = mass.a

    j = 0
    print(body.masses[j].p == masses_nparr[j]['p'])
    print(body.masses[j].p, '\n', masses_nparr[j]['p'])

    springs_nparr = np.empty(len(body.springs), dtype=spring_dtype)# %%
    ind_arr = np.arange(len(body.masses))
    for i,spring  in enumerate(body.springs):
        springs_nparr[i]['k'] = spring.k
        springs_nparr[i]['b'] = spring.b
        springs_nparr[i]['c'] = spring.c
        springs_nparr[i]['L0'] = spring.L0
        springs_nparr[i]['m1_ind'] = ind_arr[[spring.m1 == mass for mass in body.masses]][0]
        springs_nparr[i]['m2_ind'] = ind_arr[[spring.m2 == mass for mass in body.masses]][0]
        springs_nparr[i]['center'] = spring.center
        springs_nparr[i]['tissue_type'] = spring.tissue_type
        
    print(masses_nparr)
    print(masses_nparr.copy())
    
    

#%%


