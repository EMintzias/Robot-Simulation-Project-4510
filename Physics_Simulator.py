# Physics_Simulator
# UNITS MKS

import numpy as np


class Body_Simulation:
    def __init__(self, body) -> None:
        # body is an object defined in Bodies.py defining as cube for now...
        self.masses_arr = np.empty(body.size)
        self.spring_arr = np.empty(body.size)
        self.body = body  # points to the object that is being simulated

        # GLOBALS
        self.G = -9.81  # Gravity in M/S
        self.dt = 1e-4  # Time constant
        self.damping = .9999  # dont bounce forever
        self.MU_s = 1  # static friction
        self.MU_k = .8  # kinetic friction
        self.k_vertices_soft = 5000
        self.k_ground = 1e5
        self.omega = 10

        pass

    def Plot_Body(self):
        self.body.Plot()
        pass

    def Update_Forces(self):
        '''
        This function upates the forces on the springs. 
        # spring indexing as a funtion of masses is a propertu of the body

        '''
        for m in self.body.points:
            m.F = 0
            for s in m.springs:
                m.F
            pass
        pass

    ''' UPDATE POINT KINEMATICS PSUDOCODE
    def Integratoin(self, F):
        P.F = F  # this should be the vector in [Fx,Fy,Fz]

        def update_acc():
            self.acc = self.F/self.m

        def update_vel():
            self.vel += self.dt*self.acc

        def update_pos():
            self.pos += self.dt*self.vel

        self.update_acc()
        self.update_vel()
        self.update_pos()
        pass
    '''

    def run(self) -> None:
        Flag = True
        while Flag:
            Fx, Fy, Fz = self.sum_forces()

        pass


def Main():

    pass


if __name__ == "__main__":
    Main()
