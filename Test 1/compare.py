import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================
# FILE PATHS
# ============================================================

EXPERIMENTAL_FILE = r"C:\Users\jayme\Desktop\Representative_Fitted_Curve_1.xlsx"
SIMULATION_FILE = "stress_stretch.txt"

# ============================================================
# READ EXPERIMENTAL DATA
# ============================================================

exp = pd.read_excel(EXPERIMENTAL_FILE)
print("\nExperimental Columns:", list(exp.columns))

# Extract and clean experimental data
stretch_exp = exp.iloc[:, 0].astype(float).to_numpy()
stress_exp = exp.iloc[:, 1].astype(float).to_numpy()

# Baseline Zeroing: Force curve to start at 0 stress
stress_exp = stress_exp - stress_exp[0]

# ============================================================
# READ SIMULATION DATA
# ============================================================

sim = pd.read_csv(
    SIMULATION_FILE,
    sep=r"\s+",
    skiprows=1,
    names=["Stretch", "NominalStress", "TrueStress"]
)

stretch_sim = sim["Stretch"].to_numpy()
stress_sim = sim["NominalStress"].to_numpy()

# ============================================================
# CLEAN & PRE-PROCESS SIMULATION DATA
# ============================================================

# Remove NaNs
mask = np.isfinite(stretch_sim) & np.isfinite(stress_sim)
stretch_sim = stretch_sim[mask]
stress_sim = stress_sim[mask]

# Baseline Zeroing: Remove residual MD pressure so it starts at 0
stress_sim = stress_sim - stress_sim[0]

# Smooth MD thermal noise using Savitzky-Golay filter
# (Uses a window size of 51, polynomial order 3. Adjust window size if needed)
if len(stress_sim) > 51:
    stress_sim = savgol_filter(stress_sim, window_length=51, polyorder=3)

# ============================================================
# SORT & REMOVE DUPLICATES
# ============================================================

# Experimental
idx_exp = np.argsort(stretch_exp)
stretch_exp, unique_indices_exp = np.unique(stretch_exp[idx_exp], return_index=True)
stress_exp = stress_exp[idx_exp][unique_indices_exp]

# Simulation
idx_sim = np.argsort(stretch_sim)
stretch_sim, unique_indices_sim = np.unique(stretch_sim[idx_sim], return_index=True)
stress_sim = stress_sim[idx_sim][unique_indices_sim]

# ============================================================
# COMMON STRETCH RANGE
# ============================================================

xmin = max(stretch_exp.min(), stretch_sim.min())
xmax = min(stretch_exp.max(), stretch_sim.max())

print(f"\nCommon stretch range: {xmin:.3f} to {xmax:.3f}")

# Create exactly 400 evenly spaced points for a 1-to-1 comparison
stretch_common = np.linspace(xmin, xmax, 400)

# ============================================================
# INTERPOLATION
# ============================================================

exp_interp = interp1d(stretch_exp, stress_exp, kind="linear", fill_value="extrapolate")
sim_interp = interp1d(stretch_sim, stress_sim, kind="linear", fill_value="extrapolate")

stress_exp_aligned = exp_interp(stretch_common)
stress_sim_aligned = sim_interp(stretch_common)

# ============================================================
# ALIGN BASELINES & NORMALIZE (Isolating the J-Curve Shape)
# ============================================================

# Force both curves to start at exactly 0.0 at the common starting stretch
stress_exp_aligned = stress_exp_aligned - stress_exp_aligned[0]
stress_sim_aligned = stress_sim_aligned - stress_sim_aligned[0]

# We divide by the max of the ALIGNED curves so they both scale from 0 to 1
stress_exp_norm = stress_exp_aligned / np.max(np.abs(stress_exp_aligned))
stress_sim_norm = stress_sim_aligned / np.max(np.abs(stress_sim_aligned))

# ============================================================
# METRICS
# ============================================================

rmse = np.sqrt(mean_squared_error(stress_exp_norm, stress_sim_norm))
r2 = r2_score(stress_exp_norm, stress_sim_norm)

# Safe implementation of trapezoidal integration for L2 Loss
try:
    l2 = np.trapz((stress_exp_norm - stress_sim_norm)**2, stretch_common)
except AttributeError:
    l2 = np.trapezoid((stress_exp_norm - stress_sim_norm)**2, stretch_common)

# ============================================================
# PRINT & SAVE RESULTS
# ============================================================

print("\n" + "="*60)
print("Comparison Results (Shape/J-Curve Match)")
print("="*60)
print(f"RMSE     : {rmse:.6f}")
print(f"L2 Loss  : {l2:.6f}")
print(f"R2 Score : {r2:.6f}")
print("="*60)

results = pd.DataFrame({
    "Stretch": stretch_common,
    "Experimental_Norm": stress_exp_norm,
    "Simulation_Norm": stress_sim_norm
})
results.to_csv("comparison_curve.csv", index=False)

with open("comparison_results.txt", "w") as f:
    f.write("Comparison Results\n")
    f.write("=============================\n")
    f.write(f"RMSE     : {rmse:.6f}\n")
    f.write(f"L2 Loss  : {l2:.6f}\n")
    f.write(f"R2 Score : {r2:.6f}\n")

# ============================================================
# PLOT (Plotting the Aligned & Normalized Data)
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(stretch_common, stress_exp_norm, 
         linewidth=4, color='#1f77b4', label="Experimental (Target)")

plt.plot(stretch_common, stress_sim_norm, 
         '--', linewidth=3, color='#ff7f0e', label="Simulation (Smoothed)")

plt.xlabel("Stretch Ratio (λ)", fontsize=14)
plt.ylabel("Normalized Nominal Stress", fontsize=14)
plt.title("Biomechanical Mimicry: Shape Optimization", fontsize=16)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12, loc='upper left')

plt.tight_layout()
plt.savefig("comparison.png", dpi=300)
plt.show()

print("\nFiles generated: comparison.png, comparison_curve.csv, comparison_results.txt")