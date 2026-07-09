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

NUMBER_OF_CHAINS = 10

CHAIN_LENGTH = 20

BOND_LENGTH = 1.0

START_POSITION = (10.0, 10.0, 10.0)

# ==============================================================
# Simulation Box
# ==============================================================

BOX_SIZE = 60
# ==============================================================
# Packing Parameters
# ==============================================================

MIN_CHAIN_DISTANCE = 1.0

MAX_PLACEMENT_TRIES = 500


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
#-----------------------
# ==============================================================
# Renumber Atoms
# ==============================================================

# ==============================================================
# Random Chain Origin
# ==============================================================

def generate_random_origin():
    """
    Generate a random starting position for a polymer chain
    inside the simulation box.
    """

    MARGIN = 10.0

    x = random.uniform(
        MARGIN,
        BOX_SIZE - MARGIN
    )

    y = random.uniform(
        MARGIN,
        BOX_SIZE - MARGIN
    )

    z = random.uniform(
        MARGIN,
        BOX_SIZE - MARGIN
    )

    return (
        x,
        y,
        z
    )

# ==============================================================
# Inter-Chain Overlap Check
# ==============================================================

def chain_overlaps(
    candidate_atoms,
    accepted_atoms
):
    """
    Check whether a newly generated chain overlaps
    any previously accepted chain.

    Parameters
    ----------
    candidate_atoms : list
        Newly generated polymer chain.

    accepted_atoms : list
        Atoms already accepted into the polymer melt.

    Returns
    -------
    bool
        True  -> Overlap exists.
        False -> No overlap.
    """

    for candidate in candidate_atoms:

        _, _, _, x1, y1, z1 = candidate

        for accepted in accepted_atoms:

            _, _, _, x2, y2, z2 = accepted

            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2

            distance = (
                dx**2 +
                dy**2 +
                dz**2
            ) ** 0.5

            if distance < MIN_CHAIN_DISTANCE:

                return True

    return False

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

    # ----------------------------------------------------------
    # Generate multiple polymer chains
    # ----------------------------------------------------------

    for chain in range(NUMBER_OF_CHAINS):

        print(f"\nGenerating Chain {chain+1}")
    
        # ----------------------------------------------
        # Generate one SAW chain
        # ----------------------------------------------
        atoms = generate_self_avoiding_walk(
            CHAIN_LENGTH,
            BOND_LENGTH,
            START_POSITION
        )
        # ----------------------------------------------
        # Try random positions until the chain fits
        # ----------------------------------------------
        placed = False

        for attempt in range(MAX_PLACEMENT_TRIES):

            origin = generate_random_origin()

            dx = origin[0] - START_POSITION[0]

            dy = origin[1] - START_POSITION[1]

            dz = origin[2] - START_POSITION[2]

            translated_atoms = translate_atoms(
                atoms,
                dx,
                dy,
                dz
            )
            has_overlap = chain_overlaps(
                translated_atoms,
                all_atoms
            )

            if not has_overlap:
        
                atoms = translated_atoms
        
                placed = True

                print("Chain accepted")
        
                placement_attempts = attempt + 1
        
                print(
                    f"Chain {chain + 1} placed after "
                    f"{placement_attempts} attempt(s)."
                )
        
                break
        
        # ----------------------------------------------
        # Stop if no valid position was found
        # ----------------------------------------------

        if not placed:

            raise RuntimeError(
                f"Unable to place chain {chain+1}"
            )

        # ----------------------------------------------
        # Renumber atoms
        # ----------------------------------------------
            
        # Give this chain unique atom IDs and molecule ID
        atoms = renumber_atoms(
            atoms,
            atom_offset,
            chain + 1
        )       
        
        # ----------------------------------------------
        # Generate and renumber bonds
        # ----------------------------------------------

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

        # ----------------------------------------------
        # Store chain
        # ----------------------------------------------

        all_atoms.extend(atoms)
        print("Current atoms:", len(all_atoms))
        all_bonds.extend(bonds)

        atom_offset += CHAIN_LENGTH
        bond_offset += (CHAIN_LENGTH - 1)

    # ----------------------------------------------------------
    # Export LAMMPS data
    # ----------------------------------------------------------
        print(len(all_atoms))
        print(len(all_bonds))
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
    

    