#%%
from Project_Libries import *

#%%
# Point mass class
class Point_Mass:
    def __init__(self, pos, mass=.1, p_o=np.zeros(3), vel=np.zeros(3), acc=np.zeros(3), Force=np.zeros(3), ind=None):
        self.pos = np.array(pos) + p_o
        self.mass = mass
        self.vel = vel
        self.acc = acc
        self.F = Force

    def __str__(self):
        out = f'{type(self)} '
        out += f'\n\t Mass = {self.mass} Kg'
        out += f'\n\t Pos = {self.pos}'
        out += f'\n\t Vel = {self.vel}'
        out += f'\n\t Acc = {self.acc}'
        return out

#%%
# Spring class
class Spring:
    def __init__(self, Ind:tuple, L_o=.1, k=1e4):
        self.L_o = L_o
        self.K = k
        self.ind = Ind

    def __str__(self):
        out = f'{type(self)} '
        out += f'\n\t IND = {self.ind}'
        out += f'\n\t L_o = {round(self.L_o,3)} m'
        out += f'\n\t K = {round(self.K)}'
        return out


#%%
# Cube class
class Cube:
    def __init__(self, P_o=np.ones(3), cube_size=1, floor_size=4, spring_variables=(.9999, 5000, 1e4)):
        # GLOBAL VARIABLES
        self.G = -9.81  # Gravity
        self.dt = 1e-4  # Time constant
        self.T = 0      # Global Time
        # Spring Variables
        self.damping = spring_variables[0]
        self.k_edges = spring_variables[1]
        self.k_ground = spring_variables[2]

        # PLOTTING ATTRIBUTES:
        self.Floor = floor_size     # Side length of a box floor
        self.P_o = P_o              # Initial position of the first corner

        # Initialize point masses
        self.P_o = P_o
        self.Masses = np.array([
            Point_Mass(np.dot([0, 0, 0], cube_size), p_o=P_o),
            Point_Mass(np.dot([1, 0, 0], cube_size), p_o=P_o),
            Point_Mass(np.dot([1, 1, 0], cube_size), p_o=P_o),
            Point_Mass(np.dot([0, 1, 0], cube_size), p_o=P_o),
            Point_Mass(np.dot([0, 0, 1], cube_size), p_o=P_o),
            Point_Mass(np.dot([1, 0, 1], cube_size), p_o=P_o),
            Point_Mass(np.dot([1, 1, 1], cube_size), p_o=P_o),
            Point_Mass(np.dot([0, 1, 1], cube_size), p_o=P_o)
        ])
        for i, m in enumerate(self.Masses):
            m.ind = i
        self.size = self.Masses.size
        
        # Initialize springs based on the masses above
        self.initalize_springs()

        self.Forces = np.zeros(self.size)

    def initalize_springs(self):
        # Create all posible pairs (28 for cube)
        ind_arr = [(i, j) for i in range(self.size)
                   for j in range(i+1, self.size)]
        
        # Add indicees and initial length to a list of springs
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

    def init_plot(self, plot_Springs=True, plot_Shadow=True, fig=None, ax=None):
        # Update point positions to plot into this array for easier read
        P = np.array([m.pos for m in self.Masses])
        
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

        if not fig or not ax:
            # print('creating new')
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        

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
            plt.show()

        return None

    
    def update_plot(self, point_artists, line_artists):
        # Update positions of all elements
        self.Integrate_step()
        # Update point positions to plot into this array for easier read
        P = np.array([m.pos for m in self.Masses])
        
        x, y, z = zip(*P)
        point_artists._offsets3d = (x, y, z)

        # Update line positions
        all_lines = edges + springs
        for line, line_artist in zip(all_lines, line_artists):
            ex, ey, ez = zip(*line)
            line_artist.set_data(ex, ey)
            line_artist.set_3d_properties(ez)

        return point_artists, line_artists
    
    def get_F_external(self, point_mass):
        # TODO
        return np.zeros(3)

    def calc_Net_Force(self, point_mass, mass_ind):
        connected_springs = self.Springs[self.Spring_map[mass_ind]]
        F_net = np.zeros(3)
        # SPRINGS:
        '''
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
        '''
        # External:
        F_net += self.get_F_external(point_mass)

        # GRAVITY
        F_net[2] += point_mass.mass * self.G

        # GROUND:
        if point_mass.pos[2] < 0:
            # this needs to be a positive addition to raise the body
            F_net[2] += self.k_ground * -1*point_mass.pos[2]

        # print(f'F_net = {F_net}')
        return F_net

    def Integrate_step(self):
        for mass_ind, mass in enumerate(self.Masses):
            mass.F = self.calc_Net_Force(mass, mass_ind)
            mass.acc = mass.F/mass.mass
            mass.vel += mass.acc*self.dt
            mass.pos += mass.vel*self.dt

        self.T += self.dt

        return None



#%%
def main():
    # INITIALIZE CUBEs
    # Cube Variables
    damping = .9999
    k_edges = 10000
    k_ground = 1e6
    init_cube_pos = np.dot(np.ones(3), 4)
    cube_size = 1

    body = Cube(P_o=init_cube_pos, cube_size=cube_size, floor_size=4, spring_variables=(damping, k_edges, k_ground))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    point_artists, line_artists = body.init_plot(fig=fig, ax=ax)

    # Modify the update function to include the artists as arguments
    ani = FuncAnimation(fig, lambda frame: body.update_plot(point_artists, line_artists), blit=True)
    
    plt.show()


# Plot the cube 1 unit above the 5x5 floor
if __name__ == "__main__":
    main()
    # test_force()
    # Test()
