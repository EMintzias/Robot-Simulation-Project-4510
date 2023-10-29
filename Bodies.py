# %%
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
from collections import defaultdict


class Point_Mass:

    def __init__(self,
                 pos,
                 mass=.1,
                 p_o=np.zeros(3),
                 vel=np.zeros(3),
                 acc=np.zeros(3),
                 Force=np.zeros(3),
                 ind=None) -> None:
        # Intiializing position
        try:
            # Check for type errors?

            if len(pos) != 3:
                msg = ''
                msg += f"Invalid input for position: {pos}"
                msg += f'Entered an array with length = {len(pos)}'
                msg += '\n\t Should have length = 3'
                raise ValueError(msg)

            else:
                self.pos = np.array(pos) + p_o

        except ValueError as err_msg:
            print(err_msg)
            sys.exit()  # exit if there is an issue

        self.mass = mass  # in KG
        self.vel = vel
        self.acc = acc
        self.F = Force
        pass

    def __str__(self):
        out = f'{type(self)} '
        out += f'\n\t Mass = {self.mass} Kg'
        out += f'\n\t Pos = {self.pos}'
        out += f'\n\t Vel = {self.vel}'
        out += f'\n\t Acc = {self.acc}'
        return out


class Spring:
    def __init__(self, Ind: tuple,
                 L_o=.1,
                 k=1e4,
                 ) -> None:
        self.L_o = L_o
        self.K = k
        self.ind = Ind
        #self.M1_int = M1
        #self.M2_int = M2

    def __str__(self):
        out = f'{type(self)} '
        out += f'\n\t IND = {self.ind}'
        out += f'\n\t L_o = {round(self.L_o,3)} m'
        out += f'\n\t K = {round(self.K)}'
        return out


class Cube:
    # TODO Integrate this into a point object structure instead of raw positoin
    # add the indices per the below/
    def __init__(self, P_o=np.ones(3),
                 floor_size=5):
        # GLOBALS
        self.G = -9.81  # Gravity in M/S
        self.dt = 1e-4  # Time constant
        self.damping = .9999  # dont bounce forever
        self.MU_s = 1  # static friction
        self.MU_k = .8  # kinetic friction
        self.k_vertices_soft = 5000
        self.k_ground = 1e5
        self.omega = 10

        # BODY construction
        self.P_o = P_o
        self.Masses = np.array([
            Point_Mass([0, 0, 0], p_o=P_o),
            Point_Mass([1, 0, 0], p_o=P_o),
            Point_Mass([1, 1, 0], p_o=P_o),
            Point_Mass([0, 1, 0], p_o=P_o),
            Point_Mass([0, 0, 1], p_o=P_o),
            Point_Mass([1, 0, 1], p_o=P_o),
            Point_Mass([1, 1, 1], p_o=P_o),
            Point_Mass([0, 1, 1], p_o=P_o)
        ])
        for i, m in enumerate(self.Masses):
            m.ind = i

        self.size = self.Masses.size

        self.initalize_springs()  # Initialize springs based on the above

        # might store directly on point as attribute?
        self.Forces = np.zeros(self.size)

        # PLOTTING ATTRIBUTES:
        self.Floor = floor_size  # side length of a box floor
        self.P_o = P_o    # Initial position of the first corner

        pass

    def initalize_springs(self):
        # create all posible pairs (28 for cube)
        ind_arr = [(i, j) for i in range(self.size)
                   for j in range(i+1, self.size)]

        # add indicees and initial length to a list of springs
        self.Springs = np.array(np.full(len(ind_arr), None, dtype=Spring))
        for i, ind in enumerate(ind_arr):
            l_o = norm(self.Masses[ind[0]].pos - self.Masses[ind[1]].pos)
            self.Springs[i] = Spring(Ind=ind,
                                     L_o=l_o)

        # Create a dictionary to map springs to a vertex
        # i.e dict[7] returns an ind array of all the springs on the 7th mass
        self.Spring_map = {}

        Range_arr = np.arange(len(ind_arr))
        for i in range(self.size):
            ind_slice = [i in ind for ind in ind_arr]
            self.Spring_map[i] = Range_arr[ind_slice]

        return None

    def get_F_external(self, point_mass):
        return np.zeros(3)

    def calc_Net_Force(self, point_mass, mass_ind):
        connected_springs = self.Springs[self.Spring_map[mass_ind]]
        F_net = np.zeros(3)
        # SPRINGS:
        for spring in connected_springs:
            P1, P2 = self.Masses[list(spring.ind)]
            dist = norm(P2.pos-P1.pos)
            unit_vect = (P2.pos-P1.pos) / dist

            # K * distance * times a unit vector for direction givs Fs
            F_vect = spring.K * (dist-spring.L_o) * unit_vect

            # flip vector if necessary ( we calculate F from p1->p2)
            if mass_ind != spring.ind[0]:
                F_vect *= -1

            F_net += F_vect

            ''' Debug print
            
            delta  = dist-spring.L_o
            print(spring)
            out = f'Ind: {spring.ind} dist = {round(dist,2)} delta = {round(delta,2)} F_s = {round(F_scalar,2)}'
            out +=f'\n F_v = {F_vect}  \n - - - - - - -  \n'
            print(out)
            '''
        # External:
        F_net += self.get_F_external(point_mass)

        # GRAVITY
        F_net[2] += point_mass.mass * self.G

        # GROUND:
        if point_mass.pos[2] < 0:
            # this needs to be a positive addition to raise the body
            F_net[2] += self.k_ground * -1*point_mass.pos[2]

        #print(f'F_net = {F_net}')
        return F_net

    def Integrate(self):
        for mass_ind, mass in enumerate(self.Masses):
            F_net = self.calc_Net_Force(mass, mass_ind)

        return None

    # TODO add Plot method!!!


def Test():
    p_o = [1, 2, 69]
    Point = Point_Mass([0, 0, 1], p_o=p_o)
    print(Point)
    ind_arr = initialize_indices(N=8)
    print(ind_arr)
    aran = np.arange(len(ind_arr))
    ind_slice = [2 in ind for ind in ind_arr]
    print(aran[[2 in ind for ind in ind_arr]])
    springs = np.full(len(ind_arr), None, dtype=Spring)
    for i, ind in enumerate(ind_arr):
        springs[i] = Spring(Ind=ind)
    pass
    print(springs[1])


def test_force():
    body = Cube(P_o=np.zeros(3),
                floor_size=3)
    # some_cube.Plot()
    k = 1e4
    point = 2
    connected_springs = body.Springs[body.Spring_map[point]]
    body.Masses[point].pos[1] += .1  # change a bit for testing
    F_net = np.zeros(3)
    for s in connected_springs:

        print(s)
        flip = False

        P1, P2 = body.Masses[list(s.ind)]
        dist = norm(P2.pos-P1.pos)
        delta = dist-s.L_o
        F_scalar = s.K * (dist-s.L_o)
        unit_vect = (P2.pos-P1.pos) / dist
        F_vect = F_scalar*unit_vect

        # flip vector if necessary
        if point != s.ind[0]:
            flip = True
            F_vect *= -1
        F_net += F_vect
        out = f'Ind: {s.ind} dist = {round(dist,2)} delta = {round(delta,2)} F_s = {round(F_scalar,2)}'
        out += f'\n F_v = {F_vect} \nflip - {flip} \n - - - - - - -  \n'
        print(out)
    print(f'F_net = {F_net}')

    # force_vector(P1,P2)


def main():
    body = Cube(P_o=np.zeros(3),
                floor_size=3)
    point = 2
    body.Masses[point].pos[1] += .1
    rslt = body.calc_Net_Force(body.Masses[point], point)
    Integrate = body.Integrate()


# Plot the cube 1 unit above the 5x5 floor
if __name__ == "__main__":
    main()
    # test_force()
    # Test()
