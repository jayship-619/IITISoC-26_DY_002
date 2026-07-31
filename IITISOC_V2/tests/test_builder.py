from src.network.network_builder import NetworkBuilder

builder = NetworkBuilder()

network = builder.build()

print()

print("="*50)

print("NETWORK CREATED")

print("="*50)

print()

print("Chains :", len(network))

print("Beads in first chain :", network[0].n_beads)

print("Radius of Gyration :", network[0].radius_of_gyration)

print("End-to-End :", network[0].end_to_end)

print("Contour :", network[0].contour_length)

print()
