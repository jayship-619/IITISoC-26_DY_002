from src.network.network_builder import NetworkBuilder
from src.network.crosslinker import Crosslinker

builder = NetworkBuilder()

network = builder.build()

cross = Crosslinker(
    box_size=100.0,
    cutoff=1.30,
    max_links_per_bead=1
)

links = cross.build(network)

print()

print("="*50)
print("CROSSLINK TEST")
print("="*50)

print()

print("Chains :", len(network))
print("Crosslinks :", len(links))

if len(links):

    print()

    print("First five")

    for L in links[:5]:
        print(L)
