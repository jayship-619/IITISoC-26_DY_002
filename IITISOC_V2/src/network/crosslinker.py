"""
Research Version 2

Cell-list Crosslink Generator
"""

import numpy as np


class Crosslinker:

    def __init__(
        self,
        box_size,
        cutoff=1.30,
        max_links_per_bead=1,
    ):

        self.box = box_size
        self.cutoff = cutoff
        self.max_links = max_links_per_bead

    def _cell_index(self, p):

        cell = np.floor(p / self.cutoff).astype(int)

        return tuple(cell)

    def _distance(self, a, b):

        d = a - b

        d -= self.box * np.round(d / self.box)

        return np.linalg.norm(d)

    def build(self, network):

        grid = {}

        bead_info = []

        bead_id = 0

        for cid, chain in enumerate(network):

            for lid, pos in enumerate(chain.positions):

                cell = self._cell_index(pos)

                grid.setdefault(cell, []).append(bead_id)

                bead_info.append(
                    (cid, lid, pos)
                )

                bead_id += 1

        links = []

        degree = np.zeros(len(bead_info), dtype=int)

        offsets = [-1,0,1]

        for cell in grid:

            candidates = []

            cx,cy,cz = cell

            for dx in offsets:
                for dy in offsets:
                    for dz in offsets:

                        ncell = (
                            cx+dx,
                            cy+dy,
                            cz+dz
                        )

                        if ncell in grid:

                            candidates.extend(
                                grid[ncell]
                            )

            local = grid[cell]

            for i in local:

                if degree[i] >= self.max_links:
                    continue

                ci, li, pi = bead_info[i]

                for j in candidates:

                    if j <= i:
                        continue

                    if degree[j] >= self.max_links:
                        continue

                    cj, lj, pj = bead_info[j]

                    if ci == cj:
                        continue

                    d = self._distance(pi, pj)

                    if d < self.cutoff:

                        links.append(
                            (
                                ci,
                                li,
                                cj,
                                lj
                            )
                        )

                        degree[i] += 1
                        degree[j] += 1

                        break

        return links
