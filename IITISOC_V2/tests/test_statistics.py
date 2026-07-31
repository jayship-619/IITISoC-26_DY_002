from src.network.network_builder import NetworkBuilder
from src.network.crosslinker import Crosslinker
from src.analysis.statistics import NetworkStatistics

builder = NetworkBuilder()

network = builder.build()

cross = Crosslinker(
    box_size=100,
    cutoff=1.30
)

links = cross.build(network)

stats = NetworkStatistics(
    network,
    links
)

print()

print("="*50)

print("NETWORK STATISTICS")

print("="*50)

print()

for k,v in stats.summary().items():

    print(f"{k:25s}: {v}")