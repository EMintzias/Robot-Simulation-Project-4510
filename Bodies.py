# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class point_mass:

    def __init__(self,
                 mass=.1,
                 dt=1e-4,
                 pos=np.zeros(3),
                 vel=np.zeros(3),
                 acc=np.zeros(3),
                 Force=np.zeros(3),) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.F = Force
        self.dt = dt
        pass


class Springs:
    def __init__(self,
                 L_o=.005,
                 k=1,
                 M1=0,
                 M2=0) -> None:
        self.L_o = L_o
        self.K = k
        self.M1_int = M1
        self.M2_int = M2

    def force_magni(self):
        pass

    def get_M1_force():
        pass

    def Force_vector():
        # ignore structure but the thought on foce vectors is simpl: given 2 self.self.points in space, magnitude is trivial and diretion
        # p2-p1 / dis (final minus initial so this is the force on p2) natuarally the reverse of this vector is negative of that!
        # we will try to write to self.F directly from the body function or whatever is running the loop.
        pass


class Cube:
    # TODO Integrate this into a point object structure instead of raw positoin
    def __init__(self, P_o=np.ones(3),
                 floor_size=5):
        self.floor_size = floor_size
        self.points = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1]
        ]) + P_o

        self.edges = [
            [self.points[0], self.points[1], self.points[2],
                self.points[3], self.points[0]],
            [self.points[4], self.points[5], self.points[6],
                self.points[7], self.points[4]],
            [self.points[0], self.points[4]],
            [self.points[1], self.points[5]],
            [self.points[2], self.points[6]],
            [self.points[3], self.points[7]]
        ]
        self.springs = [
            [self.points[0], self.points[2]],
            [self.points[0], self.points[5]],
            [self.points[0], self.points[6]],
            [self.points[1], self.points[3]],
            [self.points[1], self.points[4]],
            [self.points[1], self.points[6]],
            [self.points[1], self.points[7]],
            [self.points[2], self.points[4]],
            [self.points[2], self.points[5]],
            [self.points[2], self.points[7]],
            [self.points[3], self.points[4]],
            [self.points[3], self.points[5]],
            [self.points[3], self.points[6]],
            [self.points[4], self.points[6]],
            [self.points[5], self.points[7]]
        ]
        self.size = self.points.size

        pass

    def Plot(self,
             plot_Springs=True,
             plot_Shadow=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot Floor
        floor = [[
            (0, 0, 0),
            (self.floor_size, 0, 0),
            (self.floor_size, self.floor_size, 0),
            (0, self.floor_size, 0)
        ]
        ]
        # Plot the floor
        floor = Poly3DCollection(floor, alpha=0.25, facecolors='g')
        ax.add_collection3d(floor)

        # Plot the 8 cube points
        x, y, z = zip(*self.points)
        ax.scatter(x, y, z, c='r', marker='o')

        # plot the springs
        if plot_Springs:
            for spring in self.springs:
                sx, sy, sz = zip(*spring)
                ax.plot(sx, sy, sz, 'y')

        # Plot the edges
        for edge in self.edges:
            ex, ey, ez = zip(*edge)
            ax.plot(ex, ey, ez, color='b')
            if plot_Shadow:
                ax.plot(ex, ey, color='grey')

        # Set axis limits based on the cube and floor size
        ax.set_xlim([0, self.floor_size])
        ax.set_ylim([0, self.floor_size])
        # 1 unit for the cube and 1 unit for the space above it
        ax.set_zlim([0, self.floor_size])

        # Set axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()

        pass

        pass


def main():
    some_cube = Cube(P_o=np.array([1, 1, 2]),
                     floor_size=3)
    some_cube.Plot()
    pass


# Plot the cube 1 unit above the 5x5 floor
if __name__ == "__main__":
    main()

# %%
