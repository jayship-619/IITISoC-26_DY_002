"""
Research Version 2

LAMMPS Data Writer
"""

from pathlib import Path

import numpy as np

class LammpsWriter:

    def __init__(self, network, crosslinks, box):

        self.network = network
        self.crosslinks = crosslinks
        self.box = box

    def write(self, filename="data/network_v2.data"):

        Path("data").mkdir(exist_ok=True)

        atom_lookup = []

        atom_id = 1

        atoms = 0
        bonds = 0
        angles = 0

        for chain in self.network:

            atoms += chain.n_beads
            bonds += chain.n_beads - 1
            angles += chain.n_beads - 2

        bonds += len(self.crosslinks)

        with open(filename, "w") as f:

            f.write("LAMMPS data file\n\n")

            f.write(f"{atoms} atoms\n")
            f.write(f"{bonds} bonds\n")
            f.write(f"{angles} angles\n\n")

            f.write("1 atom types\n")
            f.write("2 bond types\n")
            f.write("1 angle types\n\n")
            
            allp = np.vstack(
                [c.unwrapped_positions for c in self.network]
            )

            xmin = allp[:,0].min() - 2.0
            xmax = allp[:,0].max() + 2.0

            ymin = allp[:,1].min() - 2.0
            ymax = allp[:,1].max() + 2.0

            zmin = allp[:,2].min() - 2.0
            zmax = allp[:,2].max() + 2.0

            f.write(f"{xmin:.6f} {xmax:.6f} xlo xhi\n")
            f.write(f"{ymin:.6f} {ymax:.6f} ylo yhi\n")
            f.write(f"{zmin:.6f} {zmax:.6f} zlo zhi\n\n")

            f.write("Masses\n\n")
            f.write("1 1.0\n\n")

            f.write("Atoms\n\n")

            mol = 1

            for chain_no, chain in enumerate(self.network):

                ids = []

                for bead_no, p in enumerate(chain.unwrapped_positions):

                    ids.append(atom_id)

                    if chain_no == 1 and bead_no == 5:
                        print("CHAIN 1 BEAD 5 -> ATOM", atom_id)

                    if chain_no == 194 and bead_no == 29:
                        print("CHAIN 194 BEAD 29 -> ATOM", atom_id)

                    f.write(
                        f"{atom_id} "
                        f"{mol} "
                        f"1 "
                        f"{p[0]:.6f} "
                        f"{p[1]:.6f} "
                        f"{p[2]:.6f}\n"
                    )

                    atom_id += 1

                    
                atom_lookup.append(ids)

                mol += 1

            f.write("\nBonds\n\n")

            bond_id = 1

            for ids in atom_lookup:

                for i in range(len(ids)-1):

                    f.write(
                        f"{bond_id} 1 "
                        f"{ids[i]} "
                        f"{ids[i+1]}\n"
                    )

                    bond_id += 1

            print("WRITER FIRST CROSSLINK:", self.crosslinks[0])
            
            for c1,b1,c2,b2 in self.crosslinks:

                if c1 >= len(atom_lookup):
                    print("BAD CHAIN 1", c1)
                    raise SystemExit

                if c2 >= len(atom_lookup):
                    print("BAD CHAIN 2", c2)
                    raise SystemExit

                if b1 >= len(atom_lookup[c1]):
                    print("BAD BEAD 1")
                    print(c1,b1)
                    print("Chain length =",len(atom_lookup[c1]))
                    raise SystemExit

                if b2 >= len(atom_lookup[c2]):
                    print("BAD BEAD 2")
                    print(c2,b2)
                    print("Chain length =",len(atom_lookup[c2]))
                    raise SystemExit

                id1 = atom_lookup[c1][b1]
                id2 = atom_lookup[c2][b2]

                if (c1, b1, c2, b2) == self.crosslinks[0]:
                    print("DEBUG")
                    print("Crosslink :", (c1, b1, c2, b2))
                    print("Atom IDs  :", id1, id2)

                f.write(
                    f"{bond_id} 2 "
                    f"{id1} "
                    f"{id2}\n"
                )

                bond_id += 1

            f.write("\nAngles\n\n")

            angle_id = 1

            for ids in atom_lookup:

                for i in range(len(ids)-2):

                    f.write(
                        f"{angle_id} 1 "
                        f"{ids[i]} "
                        f"{ids[i+1]} "
                        f"{ids[i+2]}\n"
                    )

                    angle_id += 1

        print()
        print("====================================")
        print("LAMMPS DATA WRITTEN")
        print("====================================")
        print(filename)
