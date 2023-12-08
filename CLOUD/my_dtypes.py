#%%
import numpy as np


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



