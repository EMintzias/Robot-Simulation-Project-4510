# Physics_Simulator 
# UNITS MKS

import numpy as np

class point_mass:
    def __init__(self,mass =1e-3, ) -> None:
        self.mass = mass
        self.a = np.zeros(3)
        self.v = np.zeros(3)
        self.x = np.zeros(3)
        pass
    
    def update_v(self,a):
        pass
    
    
    def update_a(self,da):
        self.a += da
        pass

class Springs:
    
    


class Simulator:
    
    def __init__(self) -> None:
        self.dt = 1e-4
        self.T  = 0 
        
        pass
    
    
    
    
    
    
    def Interatoin(self, point_mass):
        #computes all forces connected to a point mass
        coneected_masses  = self.get_conections(point_mass)  #TODO
        for mass in coneected_masses: 
            dis
    
    def run(self) -> None:
        Flag = True
        while Flag:
            Fx,Fy,Fz = self.sum_forces()   
        
        pass
    