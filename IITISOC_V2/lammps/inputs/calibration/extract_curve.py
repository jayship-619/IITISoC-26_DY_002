import numpy as np
import matplotlib.pyplot as plt

log = "../tension.log"

L = []
P = []
STEP = []

reading = False

with open(log) as f:

    for line in f:

        if line.strip().startswith("Step"):
            reading = True
            continue

        if not reading:
            continue

        if "Loop time" in line:
            break

        s = line.split()

        # Thermo lines only
        if len(s) != 11:
            continue

        try:
            step = int(s[0])
            pxx = float(s[2])
            lx = float(s[5])   # <-- Lx is column 6
        except:
            continue

        STEP.append(step)
        L.append(lx)
        P.append(-pxx)

STEP = np.array(STEP)
L = np.array(L)
P = np.array(P)

strain = (L - L[0]) / L[0]

np.savetxt(
    "simulation_curve.csv",
    np.column_stack((strain, P)),
    delimiter=",",
    header="strain,stress",
    comments=""
)

plt.figure(figsize=(7,5))
plt.plot(strain, P, '-o', ms=3)
plt.xlabel("Engineering Strain")
plt.ylabel("Stress")
plt.grid(True)
plt.tight_layout()
plt.savefig("simulation_curve.png", dpi=300)

print("Frames extracted :", len(strain))
print("Initial Lx       :", L[0])
print("Final Lx         :", L[-1])
print("Final strain     :", strain[-1])
print("Maximum stress   :", P.max())