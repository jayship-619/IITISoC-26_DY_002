"""
====================================================================
Self Avoiding Walk (SAW) Polymer Generator
====================================================================

Author  : Abhishek Nigam
Project : Synthetic Hydrogel in LAMMPS

Description
-----------
Generates a single polymer chain using the Self-Avoiding Walk (SAW)
algorithm.

Each new bead:
1. Is exactly one bond length away from the previous bead.
2. Cannot overlap any previously placed bead.
3. Is rejected if it violates the minimum allowed distance.

Output
------
Creates a LAMMPS data file that can be simulated directly.

====================================================================
"""

# ==================================================================
# Imports
# ==================================================================

import random

from utils import (
    distance,
    random_unit_vector,
    generate_bonds,
    write_lammps_data
)

# ==================================================================
# User Parameters
# ==================================================================

CHAIN_LENGTH = 20

BOND_LENGTH = 1.0

MIN_DISTANCE = 0.9

START_POSITION = (10.0, 10.0, 10.0)

RANDOM_SEED = 42

MAX_TRIES = 100

OUTPUT_FILE = "../data/self_avoiding_walk.data"

# ==================================================================
# Collision Detection
# ==================================================================

def is_valid_position(
    candidate_position,
    atoms,
    ignore_last=True
):
    """
    Check whether a candidate bead overlaps an
    already existing bead.

    Parameters
    ----------
    candidate_position : tuple
        Proposed (x, y, z) coordinates.

    atoms : list
        Existing atoms.

    ignore_last : bool
        Ignore the most recently placed bead.
        This bead is bonded to the new bead and
        therefore should not be treated as a collision.

    Returns
    -------
    bool
        True  -> Position is valid.
        False -> Position overlaps another bead.
    """

    # --------------------------------------------------------------
    # Determine which atoms should be checked.
    # --------------------------------------------------------------

    if ignore_last and len(atoms) > 0:
        atoms_to_check = atoms[:-1]
    else:
        atoms_to_check = atoms

    # --------------------------------------------------------------
    # Compare candidate against every existing bead.
    # --------------------------------------------------------------

    for atom in atoms_to_check:

        _, _, _, x, y, z = atom

        existing_position = (x, y, z)

        if distance(candidate_position, existing_position) < MIN_DISTANCE:
            return False

    return True


# ==================================================================
# Self Avoiding Walk Generator
# ==================================================================

def generate_self_avoiding_walk(
    chain_length,
    bond_length,
    start_position
):
    """
    Generate a polymer chain using the
    Self-Avoiding Walk algorithm.
    """

    # --------------------------------------------------------------
    # Initialize random number generator
    # --------------------------------------------------------------


    atoms = []

    x, y, z = start_position

    molecule_id = 1
    atom_type = 1

    # --------------------------------------------------------------
    # Place first bead
    # --------------------------------------------------------------

    atoms.append(
        (
            1,
            molecule_id,
            atom_type,
            x,
            y,
            z
        )
    )

    # --------------------------------------------------------------
    # Generate remaining beads
    # --------------------------------------------------------------

    for atom_id in range(2, chain_length + 1):

        placed = False

        # ----------------------------------------------------------
        # Try multiple random directions until
        # a valid position is found.
        # ----------------------------------------------------------

        for _ in range(MAX_TRIES):

            # Generate random unit vector.

            dx, dy, dz = random_unit_vector()

            # Create candidate position.

            candidate = (
                x + dx * bond_length,
                y + dy * bond_length,
                z + dz * bond_length
            )

            # Accept only if it does not overlap
            # an existing bead.

            if is_valid_position(candidate, atoms):

                x, y, z = candidate

                atoms.append(
                    (
                        atom_id,
                        molecule_id,
                        atom_type,
                        x,
                        y,
                        z
                    )
                )

                placed = True

                break

        # ----------------------------------------------------------
        # Stop if no valid position can be found.
        # ----------------------------------------------------------

        if not placed:

            raise RuntimeError(
                f"Unable to place bead {atom_id} "
                f"after {MAX_TRIES} attempts."
            )

    return atoms


# ==================================================================
# Main Program
# ==================================================================

def main():
    """
    Generate polymer,
    generate bonds,
    write LAMMPS data file.
    """

    atoms = generate_self_avoiding_walk(
        CHAIN_LENGTH,
        BOND_LENGTH,
        START_POSITION
    )

    bonds = generate_bonds(
        CHAIN_LENGTH
    )

    write_lammps_data(
        OUTPUT_FILE,
        atoms,
        bonds
    )

    print("\n======================================")
    print(" Self-Avoiding Walk Generated")
    print("======================================")
    print(f"Atoms : {len(atoms)}")
    print(f"Bonds : {len(bonds)}")
    print(f"Output: {OUTPUT_FILE}")
    print("======================================\n")


# ==================================================================
# Program Entry Point
# ==================================================================

if __name__ == "__main__":
    main()