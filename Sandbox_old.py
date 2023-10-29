def Plot(self, plot_Springs=True, plot_Shadow=True):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Update points to plot into this array for easier read
    Points = np.array([m.pos for m in self.Masses])

    # Plot Floor #TODO plot dynamic floor with COM calc on body.
    COM = [np.mean(Points[:, col]) for col in range(len(Points[0]))]
    floor = [[
        (COM[0]-self.Floor/2, COM[1]-self.Floor/2, 0),
        (COM[0]+self.Floor/2, COM[1]-self.Floor/2, 0),
        (COM[0]+self.Floor/2, COM[1]+self.Floor/2, 0),
        (COM[0]-self.Floor/2, COM[1]+self.Floor/2, 0)
    ]
    ]
    # Plot the floor
    floor = Poly3DCollection(floor, alpha=0.25, facecolors='g')
    ax.add_collection3d(floor)

    # Plot the 8 cube points
    x, y, z = zip(*Points)
    ax.scatter(x, y, z, c='r', marker='o')

     edges = [
          [Points[0], Points[1], Points[2],
            Points[3], Points[0]],
          [Points[4], Points[5], Points[6],
                Points[7], Points[4]],
          [Points[0], Points[4]],
          [Points[1], Points[5]],
          [Points[2], Points[6]],
          [Points[3], Points[7]]
          ]
      springs = [
           [Points[0], Points[2]], [Points[0], Points[5]],
            [Points[0], Points[6]], [Points[1], Points[3]],
            [Points[1], Points[4]], [Points[1], Points[6]],
            [Points[1], Points[7]], [Points[2], Points[4]],
            [Points[2], Points[5]], [Points[2], Points[7]],
            [Points[3], Points[4]], [Points[3], Points[5]],
            [Points[3], Points[6]], [Points[4], Points[6]],
            [Points[5], Points[7]]
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
        ax.set_xlim([0, self.Floor])
        ax.set_ylim([0, self.Floor])
        # 1 unit for the cube and 1 unit for the space above it
        ax.set_zlim([0, self.Floor])

        # Set axis labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()

        pass
    
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


def test_force():
    body = Cube(P_o=np.zeros(3))
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
