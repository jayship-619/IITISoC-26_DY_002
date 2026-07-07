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

        molecule_id = 1
        atoms.append(
            (atom_id, molecule_id, atom_type, x, y, z)
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
# write_lammps_data
# ===========================
def write_lammps_data(filename, atoms, bonds):
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

    # print("\nAtoms\n")

    # for atom in atoms:
    #     print(atom)

    # print("\nBonds\n")

    # for bond in bonds:
    #     print(bond)

    #This is the New Addition
    write_lammps_data(
    "../data/chain.data",
    atoms,
    bonds
    )

if __name__ == "__main__":
    main()