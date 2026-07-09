"""
====================================================================
Polymer Melt Generator
====================================================================

Author  : Abhishek Nigam
Project : Synthetic Hydrogel in LAMMPS

Description
-----------
Generates multiple polymer chains and combines them into a
single LAMMPS data file.

Version 1.0
-----------
✓ Multiple chains
✓ Continuous atom IDs
✓ Continuous bond IDs
✓ Molecule IDs

Future Versions
---------------
- Random placement
- Inter-chain overlap checking
- Variable chain lengths
- Multiple polymer species

====================================================================
"""
# ==============================================================
# Imports
# ==============================================================

from self_avoiding_walk import generate_self_avoiding_walk 
import random

from utils import (
    generate_bonds,
    write_lammps_data
)
# ==============================================================
# User Parameters
# ==============================================================

NUMBER_OF_CHAINS = 2

CHAIN_LENGTH = 20

BOND_LENGTH = 1.0

START_POSITION = (10.0, 10.0, 10.0)

# ==============================================================
# Simulation Box
# ==============================================================

BOX_SIZE = 60



RANDOM_SEED = 42

OUTPUT_FILE = "../data/polymer_melt.data"
# ==============================================================
# Translate Chain
# ==============================================================

def translate_atoms(
    atoms,
    dx,
    dy,
    dz
):
    """
    Translate every atom by a fixed displacement.
    """

    translated = []

    for atom in atoms:

        atom_id, molecule_id, atom_type, x, y, z = atom

        translated.append(
            (
                atom_id,
                molecule_id,
                atom_type,
                x + dx,
                y + dy,
                z + dz
            )
        )

    return translated

# ==============================================================
# Random Chain Origin
# ==============================================================

def generate_random_origin():
    """
    Generate a random chain origin inside the simulation box.
    """

    MARGIN = 10.0

    x = random.uniform(MARGIN, BOX_SIZE - MARGIN)
    y = random.uniform(MARGIN, BOX_SIZE - MARGIN)
    z = random.uniform(MARGIN, BOX_SIZE - MARGIN)

    return (
        x,
        y,
        z
    )

#-----------------------
# ==============================================================
# Renumber Atoms
# ==============================================================

def renumber_atoms(
    atoms,
    atom_offset,
    molecule_id
):
    """
    Assign continuous atom IDs and a new molecule ID.
    """

    renumbered = []

    for atom in atoms:

        atom_id, _, atom_type, x, y, z = atom

        renumbered.append(
            (
                atom_id + atom_offset,
                molecule_id,
                atom_type,
                x,
                y,
                z
            )
        )

    return renumbered
#--------------------
# ==============================================================
# Renumber Bonds
# ==============================================================

def renumber_bonds(
    bonds,
    bond_offset,
    atom_offset
):
    """
    Assign continuous bond IDs and update atom references.
    """

    renumbered = []

    for bond in bonds:

        bond_id, bond_type, atom1, atom2 = bond

        renumbered.append(
            (
                bond_id + bond_offset,
                bond_type,
                atom1 + atom_offset,
                atom2 + atom_offset
            )
        )

    return renumbered

#-------------------------
# ==============================================================
# Main Program
# ==============================================================

def main():
    random.seed(RANDOM_SEED)

    all_atoms = []

    all_bonds = []

    atom_offset = 0

    bond_offset = 0

    for chain in range(NUMBER_OF_CHAINS):

        # Generate one polymer chain
        atoms = generate_self_avoiding_walk(
            CHAIN_LENGTH,
            BOND_LENGTH,
            START_POSITION
        )

        # # Generate a random position and translate the chain
        origin = generate_random_origin()

        dx = origin[0] - START_POSITION[0]

        dy = origin[1] - START_POSITION[1]

        dz = origin[2] - START_POSITION[2]

        print(f"\nChain {chain+1}")

        print("Origin:", origin)

        print("dx =", dx)

        print("First atom BEFORE:", atoms[0])

        atoms = translate_atoms(
            atoms,
            dx,
            dy,
            dz
            )

        print("First atom AFTER :", atoms[0])

        # Give this chain unique atom IDs and molecule ID
        atoms = renumber_atoms(
            atoms,
            atom_offset,
            chain + 1
        )

        # Generate bonds
        bonds = generate_bonds(
            CHAIN_LENGTH
        )

        # Give bonds unique IDs
        bonds = renumber_bonds(
            bonds,
            bond_offset,
            atom_offset
        )

        all_atoms.extend(atoms)
        all_bonds.extend(bonds)

        atom_offset += CHAIN_LENGTH
        bond_offset += (CHAIN_LENGTH - 1)

    # Export to LAMMPS
    write_lammps_data(
        OUTPUT_FILE,
        all_atoms,
        all_bonds,
        (BOX_SIZE, BOX_SIZE, BOX_SIZE) 
        )   

    print("\n======================================")
    print("Polymer Melt Generated Successfully")
    print("======================================")
    print(f"Chains : {NUMBER_OF_CHAINS}")
    print(f"Atoms  : {len(all_atoms)}")
    print(f"Bonds  : {len(all_bonds)}")
    print(f"Output : {OUTPUT_FILE}")
    print("======================================\n")


# ==============================================================
# Program Entry Point
# ==============================================================

if __name__ == "__main__":
    main()
    

    