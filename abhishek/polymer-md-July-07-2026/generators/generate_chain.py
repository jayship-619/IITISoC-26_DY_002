'''generate_chain.py

main()

│
├── generate_atoms()
│
├── generate_bonds()
│
├── write_lammps_data()
│
└── save()'''
"""
generate_chain.py

Purpose:
Generate a simple straight polymer chain.

This is Version 1.
Later versions will generate:
- random walk chains
- self-avoiding walks
- multiple chains
- cross-linked polymer networks

Author: Abhishek Nigam
Project: Synthetic Hydrogel in LAMMPS
"""

# ===========================
# PARAMETERS
# ===========================

CHAIN_LENGTH = 5
BOND_LENGTH = 1.0
START_POSITION = (5.0, 5.0, 5.0)


# ===========================
# GENERATE ATOMS
# ===========================

def generate_atoms(chain_length, bond_length, start_position):
    """
    Generate atom coordinates for a straight polymer chain.

    Returns:
        atoms (list)

    Format:
        (atom_id, atom_type, x, y, z)
    """

    atoms = []

    x0, y0, z0 = start_position

    for i in range(chain_length):

        atom_id = i + 1
        atom_type = 1

        x = x0 + i * bond_length
        y = y0
        z = z0

        atoms.append(
            (atom_id, atom_type, x, y, z)
        )

    return atoms


# ===========================
# GENERATE BONDS
# ===========================

def generate_bonds(chain_length):
    """
    Generate bonds between consecutive atoms.

    Returns:
        bonds (list)

    Format:
        (bond_id, bond_type, atom1, atom2)
    """

    bonds = []

    for i in range(chain_length - 1):

        bond_id = i + 1
        bond_type = 1

        atom1 = i + 1
        atom2 = i + 2

        bonds.append(
            (bond_id, bond_type, atom1, atom2)
        )

    return bonds


# ===========================
# MAIN
# ===========================

def main():

    atoms = generate_atoms(
        CHAIN_LENGTH,
        BOND_LENGTH,
        START_POSITION
    )

    bonds = generate_bonds(
        CHAIN_LENGTH
    )

    print("\nAtoms\n")

    for atom in atoms:
        print(atom)

    print("\nBonds\n")

    for bond in bonds:
        print(bond)


if __name__ == "__main__":
    main()