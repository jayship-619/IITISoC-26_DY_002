import numpy as np
import pandas as pd
import material_fingerprinting as mf

# Load experimental data
df = pd.read_csv("intact-wall.csv")

# Engineering strain
strain = df["Engineering Strain-X"].values

# Engineering stress (MPa)
eng_stress = df["Engineering Stress(MPa)-Y"].values

# Remove NaN values
mask = ~(np.isnan(strain) | np.isnan(eng_stress))
strain = strain[mask]
eng_stress = eng_stress[mask]

# Stretch ratio
F11 = 1.0 + strain

# Convert Engineering Stress -> True Stress
true_stress = eng_stress * F11

# Convert True Stress -> First Piola-Kirchhoff Stress
P11 = true_stress / F11

# (Equivalent to engineering stress)
# P11 = eng_stress

# Create measurement
measurement = mf.Measurement(
    "uniaxial tension/compression",
    F11,
    P11
)

# Discover material model
result = mf.discover([measurement])

print(result)