import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from matplotlib.ticker import AutoMinorLocator

# =====================================================
# Publication settings
# =====================================================

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 9,
    'axes.linewidth': 1.2,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.size': 5,
    'ytick.major.size': 5,
    'xtick.minor.size': 3,
    'ytick.minor.size': 3,
    'xtick.major.width': 1.1,
    'ytick.major.width': 1.1,
    'xtick.minor.width': 0.8,
    'ytick.minor.width': 0.8,
    'legend.frameon': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

# =====================================================
# Read curve
# =====================================================

def read_curve(filename):

    df = pd.read_csv(filename)

    x = df.iloc[:,0].astype(float).values
    y = df.iloc[:,1].astype(float).values

    mask = np.isfinite(x) & np.isfinite(y)

    x = x[mask]
    y = y[mask]

    idx = np.argsort(x)

    x = x[idx]
    y = y[idx]

    x, idx = np.unique(x, return_index=True)
    y = y[idx]

    return x, y


# =====================================================
# Load data
# =====================================================

x1, y1 = read_curve("B-green.csv")
x2, y2 = read_curve("intact-wall-true.csv")

# =====================================================
# Common region
# =====================================================

xmin = max(x1.min(), x2.min())
xmax = min(x1.max(), x2.max())

strain = np.linspace(xmin, xmax, 500)

# =====================================================
# Interpolation
# =====================================================

f1 = PchipInterpolator(x1, y1)
f2 = PchipInterpolator(x2, y2)

stress1 = f1(strain)
stress2 = f2(strain)

# =====================================================
# Mean ± SD
# =====================================================

mean = (stress1 + stress2) / 2

sd = np.std(
    np.vstack([stress1, stress2]),
    axis=0,
    ddof=1
)

# =====================================================
# Plot
# =====================================================

fig, ax = plt.subplots(figsize=(3.5,3.2))

# Individual curves

ax.plot(
    strain,
    stress1,
    lw=2.0,
    color="#0072B2",
    label="B-green"
)

ax.plot(
    strain,
    stress2,
    lw=2.0,
    color="#D55E00",
    label="Intact wallTrue"
)

# SD band

ax.fill_between(
    strain,
    mean-sd,
    mean+sd,
    color="0.80",
    alpha=0.35
)

# Mean curve

ax.plot(
    strain,
    mean,
    color="black",
    lw=3.2,
    label="Mean curve"
)

# =====================================================
# Axes
# =====================================================

ax.set_xlabel("Engineering strain")

ax.set_ylabel("True stress (MPa)")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(which='major', length=5, width=1.1)

ax.tick_params(which='minor', length=3)

ax.xaxis.set_minor_locator(AutoMinorLocator())

ax.yaxis.set_minor_locator(AutoMinorLocator())

ax.legend(loc="upper left")

plt.tight_layout(pad=0.5)

# =====================================================
# Save
# =====================================================

plt.savefig(
    "Publication_MeanCurve.png",
    dpi=600,
    bbox_inches="tight"
)

plt.savefig(
    "Publication_MeanCurve.pdf",
    bbox_inches="tight"
)

plt.savefig(
    "Publication_MeanCurve.svg",
    bbox_inches="tight"
)

plt.show()