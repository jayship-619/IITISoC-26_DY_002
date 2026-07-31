"""
========================================================

Topology objects

These classes define the polymer network.

Everything in the project will use these objects.

========================================================
"""

from dataclasses import dataclass, field


# ------------------------------------------------------
# Atom
# ------------------------------------------------------

@dataclass
class Atom:

    atom_id: int

    molecule_id: int

    atom_type: int = 1

    x: float = 0.0

    y: float = 0.0

    z: float = 0.0

    mass: float = 1.0

    charge: float = 0.0

    chain_id: int = -1

    crosslinked: bool = False


# ------------------------------------------------------
# Bond
# ------------------------------------------------------

@dataclass
class Bond:

    bond_id: int

    bond_type: int

    atom1: int

    atom2: int


# ------------------------------------------------------
# Polymer Chain
# ------------------------------------------------------

@dataclass
class Chain:

    chain_id: int

    atoms: list = field(default_factory=list)

    bonds: list = field(default_factory=list)


# ------------------------------------------------------
# Whole Network
# ------------------------------------------------------

@dataclass
class PolymerNetwork:

    atoms: list = field(default_factory=list)

    bonds: list = field(default_factory=list)

    chains: list = field(default_factory=list)
