'''utils.py
    distance()
    generate_bonds()
    write_lammps_data()
    random_unit_vector()

linear_chain.py
random_walk.py
self_avoiding_walk.py'''
'''
Utility functions shared across all polymer generators.
Every function in this file should be reusable.
No simulation code belongs here.
'''
#-------------------------------------------------------------------
"""
Shared utility functions for polymer generation.

Author: Abhishek Nigam
Project: Synthetic Hydrogel in LAMMPS
"""

import math
import random
from pathlib import Path
# ==========================================================
# Geometry Utilities
# ==========================================================
def distance(point1, point2):
    """
    Euclidean distance between two 3D points.
    """

    x1, y1, z1 = point1
    x2, y2, z2 = point2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2 +
        (z2 - z1) ** 2
    )
# ==========================================================
# Vector Utilities
# ==========================================================
def normalize_vector(vector):
    """
    Convert any vector into a unit vector.
    """

    dx, dy, dz = vector

    length = math.sqrt(
        dx**2 + dy**2 + dz**2
    )

    return (
        dx / length,
        dy / length,
        dz / length
    )
#-------------------------------------------------------------------
def random_unit_vector():
    """
    Generate a random direction in 3D.
    """

    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)
    dz = random.uniform(-1, 1)

    return normalize_vector(
        (dx, dy, dz)
    )
# ==========================================================
# Bond Utilities
# ==========================================================-
def generate_bonds(chain_length):
    """
    Generate bonds between consecutive beads.
    """

    bonds = []

    for i in range(chain_length - 1):

        bonds.append(
            (
                i + 1,
                1,
                i + 1,
                i + 2
            )
        )

    return bonds
#-------------------------------------------------------------------
def write_lammps_data(filename, atoms, bonds, box_size=(20,20,20)):
    """
    Write a simple LAMMPS data file.

    Parameters
    ----------
    filename : str
        Output filename

    atoms : list
        List of atom tuples

    bonds : list
        List of bond tuples
    """

    with open(filename, "w") as f:

        # -------------------------
        # Header
        # -------------------------

        f.write("LAMMPS data file\n\n")

        f.write(f"{len(atoms)} atoms\n")
        f.write(f"{len(bonds)} bonds\n\n")

        f.write("1 atom types\n")
        f.write("1 bond types\n\n")

        f.write("0.0 20.0 xlo xhi\n")
        f.write("0.0 20.0 ylo yhi\n")
        f.write("0.0 20.0 zlo zhi\n\n")

        # -------------------------
        # Masses
        # -------------------------

        f.write("Masses\n\n")

        f.write("1 1.0\n\n")

        # -------------------------
        # Atoms
        # -------------------------

        f.write("Atoms\n\n")

        for atom in atoms:

            atom_id, molecule_id, atom_type, x, y, z = atom

            f.write(
                f"{atom_id} {molecule_id} {atom_type} {x:.3f} {y:.3f} {z:.3f}\n"
            )

        # -------------------------
        # Bonds
        # -------------------------

        f.write("\n")

        f.write("Bonds\n\n")

        for bond in bonds:

            bond_id, bond_type, atom1, atom2 = bond

            f.write(
                f"{bond_id} {bond_type} {atom1} {atom2}\n"
            )

    print(f"\nLAMMPS data file written to: {filename}")

