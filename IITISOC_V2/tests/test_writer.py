from src.network.network_builder import NetworkBuilder
from src.network.crosslinker import Crosslinker
from src.simulation.lammps_writer import LammpsWriter

builder = NetworkBuilder()

network = builder.build()

cross = Crosslinker(
    box_size=100.0,
    cutoff=1.30
)

links = cross.build(network)

writer = LammpsWriter(
    network,
    links,
    100.0
)

writer.write()

print()

print("Chains      :", len(network))
print("Crosslinks  :", len(links))
