"""
Utility functions for IITISOC
"""

import numpy as np


# --------------------------------------------------------
# Random Unit Vector
# --------------------------------------------------------

def random_unit_vector():

    v = np.random.normal(size=3)
    v /= np.linalg.norm(v)

    return v


# --------------------------------------------------------
# Periodic Boundary Conditions
# --------------------------------------------------------

def wrap_position(position, box):

    x = position.copy()

    x[0] %= box.lx
    x[1] %= box.ly
    x[2] %= box.lz

    return x


# --------------------------------------------------------
# Minimum Image Convention
# --------------------------------------------------------

def minimum_image(dr, box):

    if dr[0] > box.lx / 2:
        dr[0] -= box.lx

    elif dr[0] < -box.lx / 2:
        dr[0] += box.lx

    if dr[1] > box.ly / 2:
        dr[1] -= box.ly

    elif dr[1] < -box.ly / 2:
        dr[1] += box.ly

    if dr[2] > box.lz / 2:
        dr[2] -= box.lz

    elif dr[2] < -box.lz / 2:
        dr[2] += box.lz

    return dr


# --------------------------------------------------------
# Distance under PBC
# --------------------------------------------------------

def distance(a, b, box):

    dr = a - b

    dr = minimum_image(dr, box)

    return np.linalg.norm(dr)
