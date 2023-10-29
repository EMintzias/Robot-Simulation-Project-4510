# %%
# Libraries should be defined in each module the below call is a catch all in case some are missed.
from Project_Libries import *

# SOME MODULES:
from Bodies import Cube, Point_Mass, Spring

# %%


def Test():
    mass = Point_Mass()


def main():
    some_cube = Cube(P_o=np.array([1, 2, 3]),
                     floor_size=3)
    # some_cube.Plot()
    print(type(some_cube))


if __name__ == "__main__":
    # Test()
    main()
