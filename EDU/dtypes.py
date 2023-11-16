#%%
from Libraries import *

#%%
# MASS DTYPE
mass_dtype = np.dtype([
            ('m', np.float64),
            ('p', np.float64, (3,)),
            ('v', np.float64, (3,)),
            ('a', np.float64, (3,)),
            ('springs', np.int32, (26,))
        ])

# SPRING DTYPE
spring_dtype = np.dtype([
            ('m1', np.int32),
            ('m2', np.int32),
            ('L0', np.float64),
            ('center', np.float64, (3,)),
            ('tissue_type', np.int32),
            ('k', np.float64),
            ('b', np.float64),
            ('c', np.float64)
        ])

#%%
masses = np.empty(5, dtype=mass_dtype)

#%%
print(masses[0]['springs'])

# %%
springs = np.zeros(0, dtype=spring_dtype)
# %%
print(springs)
# %%
springs.append(np.zeros(1,dtype=spring_dtype))
# %%
