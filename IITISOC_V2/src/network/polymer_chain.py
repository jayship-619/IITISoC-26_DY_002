"""
Polymer Chain
"""

import numpy as np


class PolymerChain:

    def __init__(self, chain_id):

        self.id = chain_id

        self.positions = []

        self.unwrapped_positions = []

        self.images = []

        self.crosslinks = []

    def add_bead(self, wrapped, unwrapped, image):

        self.positions.append(
            np.asarray(wrapped, dtype=float)
        )

        self.unwrapped_positions.append(
            np.asarray(unwrapped, dtype=float)
        )

        self.images.append(
            tuple(image)
        )

    @property
    def n_beads(self):

        return len(self.positions)

    @property
    def radius_of_gyration(self):

        x = np.asarray(self.unwrapped_positions)

        cm = np.mean(x, axis=0)

        return np.sqrt(
            np.mean(
                np.sum((x - cm) ** 2, axis=1)
            )
        )

    @property
    def end_to_end(self):

        return np.linalg.norm(
            self.unwrapped_positions[-1]
            - self.unwrapped_positions[0]
        )

    @property
    def contour_length(self):

        x = np.asarray(self.unwrapped_positions)

        d = np.diff(x, axis=0)

        return np.sum(
            np.linalg.norm(d, axis=1)
        )