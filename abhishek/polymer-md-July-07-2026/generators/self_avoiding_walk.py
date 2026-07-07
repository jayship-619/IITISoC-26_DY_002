import math
import random
CHAIN_LENGTH = 20

BOND_LENGTH = 1.0

START_POSITION = (10.0, 10.0, 10.0)

RANDOM_SEED = 42
def generate_random_walk(chain_length, bond_length, start_position):

    random.seed(RANDOM_SEED)

    atoms = []

    x, y, z = start_position

    molecule_id = 1

    atom_type = 1

    atoms.append(
        (1, molecule_id, atom_type, x, y, z)
    )

    for atom_id in range(2, chain_length + 1):

        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        dz = random.uniform(-1, 1)

        length = math.sqrt(
            dx**2 + dy**2 + dz**2
        )

        dx /= length
        dy /= length
        dz /= length

        x += dx * bond_length
        y += dy * bond_length
        z += dz * bond_length

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

    return atoms


def generate_bonds(chain_length):

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
atoms = generate_random_walk(
    CHAIN_LENGTH,
    BOND_LENGTH,
    START_POSITION
)

bonds = generate_bonds(
    CHAIN_LENGTH
)

write_lammps_data(
    "../data/random_walk.data",
    atoms,
    bonds
)