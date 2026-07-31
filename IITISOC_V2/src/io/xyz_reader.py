"""
XYZ Reader
"""

import numpy as np


class XYZReader:

    def __init__(self, filename):

        self.filename = filename

    def read(self):

        coords = []

        with open(self.filename) as f:

            lines = f.readlines()[2:]

        for line in lines:

            s = line.split()

            coords.append([
                float(s[1]),
                float(s[2]),
                float(s[3])
            ])

        return np.asarray(coords)
