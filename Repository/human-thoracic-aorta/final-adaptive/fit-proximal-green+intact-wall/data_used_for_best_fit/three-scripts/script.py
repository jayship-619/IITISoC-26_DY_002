import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# Publication style
# ==========================================================
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
    "legend.frameon": False,
    "figure.dpi": 150
})

# ==========================================================
# Function to read and clean data
# ==========================================================

def load_curve(filename):

    df = pd.read_csv(filename)

    # First column = Engineering strain
    # Second column = True stress

    x = df.iloc[:, 0].astype(float).values
    y = df.iloc[:, 1].astype(float).values

    # Remove NaN
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    # Sort
    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]

    # Remove duplicate strain values
    x, ind = np.unique(x, return_index=True)
    y = y[ind]

    return x, y


# ==========================================================
# Load datasets
# ==========================================================

xB, yB = load_curve("B-green.csv")
xI, yI = load_curve("intact-wall-true.csv")

# ==========================================================
# Plot
# ==========================================================

fig, ax = plt.subplots(figsize=(7, 6))

ax.plot(
    xB,
    yB,
    color="#1f77b4",
    linewidth=2.8,
    label="B-green"
)

ax.plot(
    xI,
    yI,
    color="#d62728",
    linewidth=2.8,
    label="Intact wallTrue"
)

# ==========================================================
# Labels
# ==========================================================

ax.set_xlabel("Engineering strain", fontsize=15)
ax.set_ylabel("True stress (MPa)", fontsize=15)

# ==========================================================
# Publication formatting
# ==========================================================

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(
    direction="in",
    length=6,
    width=1.3
)

ax.legend(
    loc="upper left",
    fontsize=12
)

plt.tight_layout()

# ==========================================================
# Save
# ==========================================================

plt.savefig(
    "Bgreen_vs_IntactWallTrue.png",
    dpi=600,
    bbox_inches="tight"
)

plt.savefig(
    "Bgreen_vs_IntactWallTrue.pdf",
    bbox_inches="tight"
)

plt.savefig(
    "Bgreen_vs_IntactWallTrue.svg",
    bbox_inches="tight"
)

plt.show()