import numpy as np
import math

# =============================================================
# PARAMETERS (Tuned for Strain-Stiffening J-Curve)
# =============================================================

NCHAINS = 1000                # Increased from 200 (More chains)
CHAIN_LENGTH = 10             # Decreased from 50 (Shorter, stiffer segments)

TARGET_DENSITY = 0.85         # Reduced LJ density

BOND_LENGTH = 0.97            # FENE equilibrium bond length

REACTIVE_FRACTION = 0.30      # Increased from 0.15 (Higher crosslink density)

SEED = 12345

np.random.seed(SEED)

# =============================================================
# DERIVED PARAMETERS
# =============================================================

TOTAL_ATOMS = NCHAINS * CHAIN_LENGTH

BOX = (TOTAL_ATOMS / TARGET_DENSITY) ** (1.0 / 3.0)

TOTAL_BACKBONE_BONDS = NCHAINS * (CHAIN_LENGTH - 1)

# =============================================================
# STORAGE
# =============================================================

atoms = []
bonds = []

atom_id = 1
bond_id = 1

reactive_count = 0

# =============================================================
# RANDOM UNIT VECTOR
# =============================================================

def random_direction():

    phi = np.random.uniform(0.0, 2.0*np.pi)

    cos_theta = np.random.uniform(-1.0, 1.0)

    sin_theta = np.sqrt(1.0 - cos_theta**2)

    return np.array([
        sin_theta*np.cos(phi),
        sin_theta*np.sin(phi),
        cos_theta
    ])

# =============================================================
# GRID OF STARTING POSITIONS
# =============================================================

grid = math.ceil(NCHAINS ** (1/3))

spacing = BOX / grid

start_positions = []

for i in range(grid):
    for j in range(grid):
        for k in range(grid):

            if len(start_positions) >= NCHAINS:
                break

            jitter = np.random.uniform(
                -0.20*spacing,
                 0.20*spacing,
                 size=3
            )

            pos = np.array([
                (i+0.5)*spacing,
                (j+0.5)*spacing,
                (k+0.5)*spacing
            ]) + jitter

            pos %= BOX

            start_positions.append(pos)

# =============================================================
# BUILD POLYMER CHAINS
# =============================================================

for mol in range(NCHAINS):

    pos = start_positions[mol].copy()

    previous_atom = None

    for bead in range(CHAIN_LENGTH):

        if np.random.rand() < REACTIVE_FRACTION:

            atom_type = 2
            reactive_count += 1

        else:

            atom_type = 1

        atoms.append([
            atom_id,
            mol+1,
            atom_type,
            pos[0],
            pos[1],
            pos[2]
        ])

        if previous_atom is not None:

            bonds.append([
                bond_id,
                1,
                previous_atom,
                atom_id
            ])

            bond_id += 1

        previous_atom = atom_id

        atom_id += 1

        direction = random_direction()

        pos = pos + direction*BOND_LENGTH

        pos %= BOX

# =============================================================
# WRITE LAMMPS DATA FILE
# =============================================================

with open("linear_melt.data","w") as f:

    f.write("LAMMPS Polymer Melt\n\n")

    f.write(f"{TOTAL_ATOMS} atoms\n")
    f.write(f"{TOTAL_BACKBONE_BONDS} bonds\n\n")

    f.write("2 atom types\n")
    f.write("2 bond types\n\n")

    f.write(f"0.0 {BOX:.6f} xlo xhi\n")
    f.write(f"0.0 {BOX:.6f} ylo yhi\n")
    f.write(f"0.0 {BOX:.6f} zlo zhi\n\n")

    f.write("Masses\n\n")

    f.write("1 1.0\n")
    f.write("2 1.0\n\n")

    f.write("Atoms\n\n")

    for a in atoms:

        f.write(
            f"{a[0]} {a[1]} {a[2]} "
            f"{a[3]:.6f} {a[4]:.6f} {a[5]:.6f}\n"
        )

    f.write("\nBonds\n\n")

    for b in bonds:

        f.write(
            f"{b[0]} {b[1]} {b[2]} {b[3]}\n"
        )

# =============================================================
# SUMMARY
# =============================================================

print("="*55)

print(" Polymer Melt Successfully Generated")

print("="*55)

print(f"Chains              : {NCHAINS}")
print(f"Chain Length        : {CHAIN_LENGTH}")

print(f"Atoms               : {TOTAL_ATOMS}")

print(f"Backbone Bonds      : {TOTAL_BACKBONE_BONDS}")

print(f"Reactive Sites      : {reactive_count}")

print(f"Target Density      : {TARGET_DENSITY:.3f}")

print(f"Computed Box Length : {BOX:.3f}")

print(f"Output File         : linear_melt.data")

print("="*55)