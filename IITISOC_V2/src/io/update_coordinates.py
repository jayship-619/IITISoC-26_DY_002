"""
Update Network Coordinates
"""

import numpy as np


class CoordinateUpdater:

    def __init__(self, network):
        self.network = network

    def apply(self, xyz):

        k = 0

        for chain in self.network:

            image = np.zeros(3, dtype=int)

            chain.images = []

            chain.unwrapped_positions = []

            for i in range(chain.n_beads):

                p = np.asarray(xyz[k], dtype=float)

                chain.positions[i] = p.copy()

                if i == 0:

                    chain.unwrapped_positions.append(p.copy())

                    chain.images.append((0, 0, 0))

                else:

                    prev = chain.positions[i-1]

                    delta = p - prev

                    for d in range(3):

                        if delta[d] > 50.0:
                            image[d] -= 1

                        elif delta[d] < -50.0:
                            image[d] += 1

                    unwrap = p + image * 100.0

                    chain.unwrapped_positions.append(unwrap)

                    chain.images.append(tuple(image))

                k += 1

        return self.network