from src.network.network_builder import NetworkBuilder
from src.io.xyz_reader import XYZReader
from src.io.update_coordinates import CoordinateUpdater

builder = NetworkBuilder()

network = builder.build()

reader = XYZReader("data/packed/network_packed.xyz")

xyz = reader.read()

CoordinateUpdater(network).apply(xyz)

print()

print("First bead")
print(network[0].positions[0])

print()

print("Last bead")
print(network[-1].positions[-1])
