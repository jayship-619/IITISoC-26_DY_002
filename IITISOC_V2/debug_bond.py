from math import sqrt

atoms = {}
bonds = []

section = None

with open("data/lammps/network_v2.data") as f:

    for line in f:

        line = line.strip()

        if line == "Atoms":
            section = "atoms"
            next(f)
            continue

        if line == "Bonds":
            section = "bonds"
            next(f)
            continue

        if line == "Angles":
            break

        if line == "":
            continue

        if section == "atoms":

            s = line.split()

            if len(s) < 6:
                continue

            ID = int(s[0])

            atoms[ID] = (
                float(s[3]),
                float(s[4]),
                float(s[5])
            )

        elif section == "bonds":

            s = line.split()

            if len(s) < 4:
                continue

            bonds.append(
                (
                    int(s[2]),
                    int(s[3])
                )
            )

print("Atoms:",len(atoms))
print("Bonds:",len(bonds))

target = (148,1384)

for b in bonds:

    if set(b)==set(target):

        print("\nFOUND BOND\n")

        a = atoms[b[0]]
        c = atoms[b[1]]

        print("Atom1",b[0],a)
        print("Atom2",b[1],c)

        d = sqrt(
            (a[0]-c[0])**2+
            (a[1]-c[1])**2+
            (a[2]-c[2])**2
        )

        print("Distance =",d)
