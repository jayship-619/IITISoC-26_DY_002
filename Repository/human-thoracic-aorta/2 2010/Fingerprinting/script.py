import numpy as np
import pandas as pd
import material_fingerprinting as mf

# Load experimental data
df = pd.read_csv("Datasets 2010   - 2010 5bmanual.csv")

# Stretch (Deformation Gradient F11)
F11 = df["Stretch(λ)"].values

# Cauchy Stress (kPa)
cauchy_stress = df["CauchyStress(σ)(kPa)"].values

# Remove NaN values
mask = ~(np.isnan(F11) | np.isnan(cauchy_stress))
F11 = F11[mask]
cauchy_stress = cauchy_stress[mask]

# Convert kPa -> MPa (recommended)
cauchy_stress = cauchy_stress / 1000.0

# Convert Cauchy Stress -> First Piola-Kirchhoff Stress
P11 = cauchy_stress / F11

# Create measurement
measurement = mf.Measurement(
    "uniaxial tension/compression",
    F11,
    P11
)

# Discover material model
result = mf.discover([measurement])

print(result)