import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# =====================================================
# Publication style
# =====================================================
plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.linewidth": 1.5,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 1.3,
    "ytick.major.width": 1.3,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "legend.frameon": False
})

# =====================================================
# Function to read and clean data
# =====================================================

def load_curve(filename):

    df = pd.read_csv(filename)

    x = df.iloc[:,0].astype(float).values
    y = df.iloc[:,1].astype(float).values

    # Remove NaN
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    # Sort
    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]

    # Remove duplicate x values
    x, idx = np.unique(x, return_index=True)
    y = y[idx]

    return x, y

# =====================================================
# Load curves
# =====================================================

x1, y1 = load_curve("B-purple.csv")
x2, y2 = load_curve("intact-wall-true.csv")

# =====================================================
# Common strain interval
# =====================================================

xmin = max(x1.min(), x2.min())
xmax = min(x1.max(), x2.max())

strain = np.linspace(xmin, xmax, 500)

# =====================================================
# Shape-preserving interpolation
# =====================================================

f1 = PchipInterpolator(x1, y1)
f2 = PchipInterpolator(x2, y2)

stress1 = f1(strain)
stress2 = f2(strain)

# =====================================================
# Mean and SD
# =====================================================

mean_stress = (stress1 + stress2) / 2

sd = np.std(
    np.vstack([stress1, stress2]),
    axis=0,
    ddof=1
)

# =====================================================
# Plot
# =====================================================

fig, ax = plt.subplots(figsize=(7,6))

# Original curves

ax.plot(
    x1,
    y1,
    color="#1f77b4",
    linewidth=2,
    alpha=0.75,
    label="B-green"
)

ax.plot(
    x2,
    y2,
    color="#d62728",
    linewidth=2,
    alpha=0.75,
    label="Intact wallTrue"
)

# Mean ± SD

ax.fill_between(
    strain,
    mean_stress-sd,
    mean_stress+sd,
    color="lightgray",
    alpha=0.4,
    label="± SD"
)

# Mean curve

ax.plot(
    strain,
    mean_stress,
    color="black",
    linewidth=3,
    label="Mean curve"
)

# =====================================================
# Formatting
# =====================================================

ax.set_xlabel("Engineering strain")
ax.set_ylabel("True stress (MPa)")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(length=6, width=1.3)

ax.legend()

plt.tight_layout()

# =====================================================
# Save
# =====================================================

plt.savefig(
    "MeanCurve_B_IntactTrue.png",
    dpi=600,
    bbox_inches="tight"
)

plt.savefig(
    "MeanCurve_B_IntactTrue.pdf",
    bbox_inches="tight"
)

plt.savefig(
    "MeanCurve_B_IntactTrue.svg",
    bbox_inches="tight"
)

plt.show()