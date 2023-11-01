#%%
from Project_Libries import *

from Bodies import Cube, Point_Mass, Spring

#%%
# Physics Simulator
# UNITS MKS
class Body_Simulation:
    def __init__(self, num_cubes= 1, P_o=np.ones(3), floor_size=4):
        # GLOBAL VARIABLES
        self.G = -9.81          # Gravity in M/S
        self.dt = 1e-4          # Time constant
        self.T = 0              # Global time

        # INITIALIZE CUBEs
        # Cube Variables
        damping = .9999
        k_edges = 10000
        k_ground = 1e6
        init_cube_pos = np.dot(np.ones(3), 4)
        cube_size = 1

        # TODO for i in num_cubes:
        cube_1 = Cube(P_o=init_cube_pos, cube_size=cube_size, floor_size=4, spring_variables=(damping, k_edges, k_ground))

    
    def animation(self):
        pass




    def Integrate_step(self, Verbose=False):
        pass



#%%
sim = Body_Simulation()


#%%

def main():

    pass


if __name__ == "__main__":
    main()
