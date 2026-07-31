from src.network.network_builder import NetworkBuilder
from src.io.xyz_writer import XYZWriter

builder = NetworkBuilder()

network = builder.build()

writer = XYZWriter(network)

writer.write()
