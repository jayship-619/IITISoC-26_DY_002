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

Output:
--------
A list of atom tuples that can be exported to a LAMMPS data file.

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

# ==================================================================
# Collision Detection
# ==================================================================

def is_valid_position(candidate_position, atoms,ignore_last=True):
    if ignore_last and len(atoms) > 0:
        atoms_to_check = atoms[:-1]
    else:
        atoms_to_check = atoms
    """
    Check whether the candidate bead overlaps
    any previously placed bead.

    Parameters
    ----------
    candidate_position : tuple
        (x, y, z) coordinates of proposed bead.

    atoms : list
        Existing atom list.

    Returns
    -------
    bool
        True  -> Position is acceptable.
        False -> Position overlaps an existing bead.
    """

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
    Generate a polymer chain using
    the Self Avoiding Walk algorithm.
    """

    random.seed(RANDOM_SEED)

    atoms = []

    x, y, z = start_position

    molecule_id = 1
    atom_type = 1

    # --------------------------------------------------------------
    # Place First Bead
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
    # Place Remaining Beads
    # --------------------------------------------------------------

    for atom_id in range(2, chain_length + 1):

        placed = False

        # Try different directions until
        # a valid position is found.

        for attempt in range(MAX_TRIES):

            # Generate a random direction.

            dx, dy, dz = random_unit_vector()

            # Create candidate position.

            candidate = (
                x + dx * bond_length,
                y + dy * bond_length,
                z + dz * bond_length
            )

            # Check whether candidate overlaps
            # an existing bead.

            if is_valid_position(candidate, atoms):

                # Accept candidate.

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

        # If no valid position was found,
        # terminate with an informative error.

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
    Generate polymer chain,
    create bonds,
    and export to LAMMPS.
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
        "../data/self_avoiding_walk.data",
        atoms,
        bonds
    )

    print("\nSelf-Avoiding Walk generated successfully.")


# ==================================================================
# Program Entry Point
# ==================================================================

if __name__ == "__main__":
    main()