from src.analysis.network_validator import NetworkValidator
from src.network.network_builder import NetworkBuilder
from src.network.crosslinker import Crosslinker
from src.io.xyz_writer import XYZWriter
from src.io.xyz_reader import XYZReader
from src.io.update_coordinates import CoordinateUpdater
from src.simulation.lammps_writer import LammpsWriter

BOX = 100.0

print("="*60)
print("BUILDING NETWORK")
print("="*60)

builder = NetworkBuilder(box_size=BOX)

network = builder.build()

XYZWriter(network).write("data/raw/network.xyz")

xyz = XYZReader("data/raw/network.xyz").read()

network = CoordinateUpdater(network).apply(xyz)

crosslinks = Crosslinker(
    box_size=100.0,
    cutoff=1.30,
    max_links_per_bead=1,
).build(network)

print("FIRST CROSSLINK:", crosslinks[0])

writer = LammpsWriter(
    network,
    crosslinks,
    100.0,
)

print("FIRST CROSSLINK:", crosslinks[0])

writer.write("data/lammps/network_v2.data")


print()
print("DONE")
