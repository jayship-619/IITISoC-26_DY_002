"""
===============================================================

IITISOC 2026

Network Generator

Author:
Kavyansh Raj Singh
IIT Indore

---------------------------------------------------------------

Purpose
-------

Generate coarse-grained polymer chains in 3D.

(Current version)

✓ Random polymer chains

Future versions

✓ Crosslinking
✓ Network topology
✓ Defective networks
✓ Star polymers
✓ Export to LAMMPS

===============================================================
"""

import numpy as np
from dataclasses import dataclass
from pathlib import Path


# =============================================================
# Simulation Box
# =============================================================

@dataclass
class SimulationBox:

    lx: float
    ly: float
    lz: float

    def random_position(self):

        return np.array([
            np.random.uniform(0, self.lx),
            np.random.uniform(0, self.ly),
            np.random.uniform(0, self.lz)
        ])


# =============================================================
# Polymer Parameters
# =============================================================

@dataclass
class PolymerParameters:

    number_of_chains: int = 100

    beads_per_chain: int = 25

    bond_length: float = 1.0

    persistence_length: float = 2.0


# =============================================================
# Polymer Chain
# =============================================================

class PolymerChain:

    def __init__(self):

        self.positions = []

    def add_bead(self, position):

        self.positions.append(np.asarray(position))

    def as_numpy(self):

        return np.array(self.positions)

    def __len__(self):

        return len(self.positions)


# =============================================================
# Network Generator
# =============================================================

class NetworkGenerator:

    def __init__(self, box, params):

        self.box = box

        self.params = params

        self.chains = []

    # ---------------------------------------------------------

    def random_unit_vector(self):

        vec = np.random.normal(size=3)

        vec /= np.linalg.norm(vec)

        return vec

    # ---------------------------------------------------------

    def generate_chain(self):

        chain = PolymerChain()

        pos = self.box.random_position()

        chain.add_bead(pos)

        direction = self.random_unit_vector()

        for i in range(self.params.beads_per_chain - 1):

            direction += (
                np.random.normal(scale=0.3, size=3)
                / self.params.persistence_length
            )

            direction /= np.linalg.norm(direction)

            pos = pos + self.params.bond_length * direction

            chain.add_bead(pos)

        return chain

    # ---------------------------------------------------------

    def generate(self):

        self.chains = []

        for i in range(self.params.number_of_chains):

            self.chains.append(self.generate_chain())

        return self.chains


# =============================================================
# Main
# =============================================================

if __name__ == "__main__":

    np.random.seed(42)

    box = SimulationBox(

        lx=100,
        ly=100,
        lz=100
    )

    params = PolymerParameters(

        number_of_chains=200,

        beads_per_chain=30,

        bond_length=1.0,

        persistence_length=2.5
    )

    network = NetworkGenerator(box, params)

    chains = network.generate()

    print()

    print("======================================")

    print("NETWORK GENERATED")

    print("======================================")

    print()

    print("Chains:", len(chains))

    print("Beads / chain:", params.beads_per_chain)

    print("Total beads:", len(chains) * params.beads_per_chain)

    print()

    print("Done.")
