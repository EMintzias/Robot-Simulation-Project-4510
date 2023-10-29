# %%
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
from collections import defaultdict
from matplotlib.animation import FuncAnimation


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
                 floor_size=4):
        # GLOBALS
        self.G = -9.81  # Gravity in M/S
        self.dt = 1e-4  # Time constant
        self.T = 0
        self.damping = .9999  # dont bounce forever
        self.MU_s = 1  # static friction
        self.MU_k = .8  # kinetic friction
        self.k_vertices_soft = 5000
        self.k_ground = 1e3
        self.omega = 10

        # PLOTTING ATTRIBUTES:
        self.Floor = floor_size  # side length of a box floor
        self.P_o = P_o    # Initial position of the first corner

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
        # TODO
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

    def Integrate_step(self):
        for mass_ind, mass in enumerate(self.Masses):
            F = self.calc_Net_Force(mass, mass_ind)
            mass.acc = F/mass.mass
            mass.vel += mass.acc*self.dt
            mass.pos += mass.vel*self.dt

        self.T += self.dt
        return None

    def Plot(self, plot_Springs=True, plot_Shadow=True, fig=None, ax=None):

        if not fig or not ax:
            #print('creating new')
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        # Update point positions to plot into this array for easier read
        P = np.array([m.pos for m in self.Masses])

        # Plot Floor #TODO universal
        COM = [np.mean(P[:, col]) for col in range(len(P[0]))]
        self.COM = COM
        floor = [[
            (COM[0]-self.Floor/2, COM[1]-self.Floor/2, 0),
            (COM[0]+self.Floor/2, COM[1]-self.Floor/2, 0),
            (COM[0]+self.Floor/2, COM[1]+self.Floor/2, 0),
            (COM[0]-self.Floor/2, COM[1]+self.Floor/2, 0)]
        ]
        # Plot the floor
        floor = Poly3DCollection(floor, alpha=0.25, facecolors='g')
        ax.add_collection3d(floor)

        # Plot the 8 cube points
        x, y, z = zip(*P)
        ax.scatter(x, y, z, c='r', marker='o')

        # Plot Lines
        edges = [
            [P[0], P[1], P[2], P[3], P[0]],
            [P[4], P[5], P[6], P[7], P[4]],
            [P[0], P[4]],
            [P[1], P[5]],
            [P[2], P[6]],
            [P[3], P[7]]
        ]
        springs = [
            [P[0], P[2]], [P[0], P[5]], [P[0], P[6]],
            [P[1], P[3]], [P[1], P[4]], [P[1], P[6]],
            [P[1], P[7]], [P[2], P[4]], [P[2], P[5]],
            [P[2], P[7]], [P[3], P[4]], [P[3], P[5]],
            [P[3], P[6]], [P[4], P[6]], [P[5], P[7]]
        ]

        # plot the springs
        if plot_Springs:
            for spring in springs:
                sx, sy, sz = zip(*spring)
                ax.plot(sx, sy, sz, 'y')

        # Plot the edges
        for edge in edges:
            ex, ey, ez = zip(*edge)
            ax.plot(ex, ey, ez, color='b')
            if plot_Shadow:
                ax.plot(ex, ey, color='grey')

        # Set axis limits based on the cube and floor size
        ax.set_xlim([COM[0]-self.Floor/2, COM[0]+self.Floor/2])
        ax.set_ylim([COM[1]-self.Floor/2, COM[1]+self.Floor/2])
        # 1 unit for the cube and 1 unit for the space above it
        ax.set_zlim([0, self.Floor])

        # Set axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        if not fig or not ax:
            # print('showing')
            plt.show()

        pass

    def Run_Animation(self, T_max=1):
        '''
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.Plot(fig = self.fig, ax = self.ax)
        plt.pause(2)
        print(self.fig,self.ax)
        self.ax.cla()
        print(self.fig,self.ax)

        '''
        i = 0
        while self.T < T_max:
            if i % 10 == 0:
                self.Plot()
                plt.pause(.001)

            self.Integrate_step()

            i += 1


def main():
    body = Cube(P_o=np.ones(3),
                floor_size=5)

    # body.Plot()
    body.Run_Animation()


# Plot the cube 1 unit above the 5x5 floor
if __name__ == "__main__":
    main()
    # test_force()
    # Test()
# %%
       for _ in range(100):
            self.Integrate_step()
        self.Plot(fig = fig, ax = ax)
