"""
Research V2

Network Statistics
"""

import numpy as np


class NetworkStatistics:

    def __init__(self, network, crosslinks):

        self.network = network
        self.crosslinks = crosslinks

    def number_of_chains(self):

        return len(self.network)

    def number_of_beads(self):

        return sum(c.n_beads for c in self.network)

    def number_of_crosslinks(self):

        return len(self.crosslinks)

    def average_chain_length(self):

        return np.mean(
            [c.n_beads for c in self.network]
        )

    def average_radius_of_gyration(self):

        return np.mean(
            [c.radius_of_gyration for c in self.network]
        )

    def average_end_to_end(self):

        return np.mean(
            [c.end_to_end for c in self.network]
        )

    def average_contour(self):

        return np.mean(
            [c.contour_length for c in self.network]
        )

    def crosslink_density(self):

        beads = self.number_of_beads()

        return len(self.crosslinks)/beads

    def summary(self):

        return {

            "Chains":
            self.number_of_chains(),

            "Beads":
            self.number_of_beads(),

            "Crosslinks":
            self.number_of_crosslinks(),

            "Crosslink Density":
            self.crosslink_density(),

            "Average Chain Length":
            self.average_chain_length(),

            "Average Rg":
            self.average_radius_of_gyration(),

            "Average Ree":
            self.average_end_to_end(),

            "Average Contour":
            self.average_contour()

        }
