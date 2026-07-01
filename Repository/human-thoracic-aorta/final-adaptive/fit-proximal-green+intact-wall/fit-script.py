import numpy as np
import pandas as pd
import material_fingerprinting as mf

# Load the experimental data
data = pd.read_csv("fit-data.csv")

# Convert engineering strain to stretch ratio
# lambda = 1 + engineering strain
F11 = 1.0 + data["Engineering Strain X"].to_numpy()

# True stress (MPa)
P11 = data["True Stress(MPa)"].to_numpy()

# Create a uniaxial measurement
measurement = mf.Measurement(
    "uniaxial tension/compression",
    F11,
    P11
)

# Discover constitutive model
mf.discover(
    [measurement],
    database="HEIIA",
    adaptive_strategy="factor",
    n_adaptive=10,
    adaptive_factor=0.5
)