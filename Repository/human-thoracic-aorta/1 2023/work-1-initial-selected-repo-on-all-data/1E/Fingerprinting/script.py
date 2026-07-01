import numpy as np
import pandas as pd
import material_fingerprinting as mf

# Load experimental data
# df = pd.read_csv("fig-1-1-red.csv")
# df = pd.read_csv("fig-1-2-blue.csv")
# df = pd.read_csv("fig-1-3-purple.csv")
df = pd.read_csv("fig-1-4-green.csv")

# Engineering strain
strain = df["Engineering Strain X"].values

# True stress (MPa)
true_stress = df["True Stress(MPa) Y"].values

# Remove any NaN values
mask = ~(np.isnan(strain) | np.isnan(true_stress))
strain = strain[mask]
true_stress = true_stress[mask]

# Deformation gradient
F11 = 1.0 + strain

# Convert True Stress -> First Piola-Kirchhoff Stress
P11 = true_stress / F11

# Create measurement
measurement = mf.Measurement(
    "uniaxial tension/compression",
    F11,
    P11
)

# Discover material model
result = mf.discover([measurement])

print(result)