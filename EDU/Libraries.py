import timeit
from tqdm import tqdm
import numpy as np
from numpy.linalg import norm
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
limit = 2000
sys.setrecursionlimit(limit)
import pdb
import math as m
import pandas as pd
import time
import threading
import datetime
import pickle
import os
import random
# NUMBA (C-python)
from numba import jit, prange, float64
# Parallelization & debugging runtime
import cProfile
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
# pyOpenGL
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# matplotlib animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import pstats
from numba import jit
import random
import copy

