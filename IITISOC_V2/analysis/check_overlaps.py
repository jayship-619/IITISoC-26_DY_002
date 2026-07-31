import numpy as np
from scipy.spatial import cKDTree

coords = []

with open("data/lammps/network_v2.data") as f:

    section = False

    for line in f:

        line = line.strip()

        if line == "Atoms":
            section = True
            next(f)
            continue

        if line == "Bonds":
            break

        if section and line:

            s = line.split()

            coords.append([
                float(s[3]),
                float(s[4]),
                float(s[5])
            ])

coords = np.asarray(coords)

tree = cKDTree(coords)

pairs = tree.query_pairs(r=0.8)

print("Pairs closer than 0.8 sigma:", len(pairs))

mind = 1e9

for i in range(len(coords)):

    d, j = tree.query(coords[i], k=2)

    if d[1] < mind:
        mind = d[1]

print("Minimum separation:", mind)
