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

# %%
springs_nparr = np.empty(len(body.springs), dtype=spring_dtype)# %%

for i,spring  in enumerate(body.springs):
    springs_nparr[i]['k'] = spring.k
    springs_nparr[i]['b'] = spring.b
    springs_nparr[i]['c'] = spring.c
    springs_nparr[i]['L0'] = spring.L0
    #springs_nparr[i]['m1_ind'] = np.where(body.masses == spring.m1)[0][0]
    #springs_nparr[i]['m2_ind'] = np.where(body.masses == spring.m2)[0][0]
    springs_nparr[i]['center'] = spring.center
    springs_nparr[i]['tissue_type'] = spring.tissue_type
    


  
    

# %%

s2 = body.springs[2]
print(s2.m1 == body.masses)

for mass in body.masses: 
    if s2.m1 == mass or s2.m2 == mass:
        print('True')
    else: print('False')

# %%
import numpy as np

# Example NumPy array
arr = np.array([1, 2, 3, 4, 5])

# Value to find
value_to_find = 3

# Find the index
indices = np.where(arr == value_to_find)[0][0]

# Print the result
print(f"Index/Indices of {value_to_find} in the array: {indices}")

# %%
