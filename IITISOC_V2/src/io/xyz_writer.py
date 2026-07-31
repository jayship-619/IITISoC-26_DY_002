"""
XYZ Writer
"""

from pathlib import Path


class XYZWriter:

    def __init__(self, network):

        self.network = network

    def write(self, filename="data/raw/network.xyz"):

        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        atoms = sum(chain.n_beads for chain in self.network)

        with open(filename, "w") as f:

            f.write(f"{atoms}\n")
            f.write("Polymer Network\n")

            for chain in self.network:

                for p in chain.positions:

                    f.write(
                        f"C {p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n"
                    )

        print()
        print("XYZ written ->", filename)
