import matplotlib.pyplot as plt
import numpy as np

from network_generator import (
    NetworkGenerator,
    SimulationBox,
    PolymerParameters,
)

import config


box = SimulationBox(

    config.BOX_X,

    config.BOX_Y,

    config.BOX_Z

)

params = PolymerParameters(

    number_of_chains=config.NUMBER_OF_CHAINS,

    beads_per_chain=config.BEADS_PER_CHAIN,

    bond_length=config.BOND_LENGTH,

    persistence_length=config.PERSISTENCE_LENGTH,

    minimum_distance=config.MINIMUM_DISTANCE,

    max_attempts=config.MAX_ATTEMPTS

)

network = NetworkGenerator(

    box,

    params

)

chains = network.generate()


fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(111, projection="3d")

for chain in chains:

    xyz = np.array(chain.positions)

    ax.plot(

        xyz[:,0],

        xyz[:,1],

        xyz[:,2],

        lw=0.5

    )

ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")

plt.tight_layout()

plt.show()
