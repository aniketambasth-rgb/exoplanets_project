import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the unified catalog
merged = pd.read_csv("unified_exoplanets.csv", low_memory=False)

# Filter out missing values
data = merged[["mass", "radius"]].dropna()
data = data[(data["mass"] > 0) & (data["radius"] > 0)]
data = data[(data["mass"] >= 0.01) & (data["mass"] <= 20000)]

# Work in log space
x = np.log10(data["mass"].values)
y = np.log10(data["radius"].values)

# Breakpoints in log space
b1 = np.log10(10)    # 10  Earth masses
b2 = np.log10(100)   # 100 Earth masses

# Build the design matrix for connected piecewise linear fit:
# y = a + s1*x + s2*max(x-b1, 0) + s3*max(x-b2, 0)
A = np.column_stack([
    np.ones_like(x),          # intercept
    x,                         # base slope (region 1)
    np.maximum(x - b1, 0),    # slope change at b1
    np.maximum(x - b2, 0),    # slope change at b2
])

# Least squares fit (minimizes chi-square)
coeffs, residuals, rank, sv = np.linalg.lstsq(A, y, rcond=None)
a, s1, ds2, ds3 = coeffs

slope1 = s1
slope2 = s1 + ds2
slope3 = s1 + ds2 + ds3

print(f"Region 1 slope (rocky):     {slope1:.3f}")
print(f"Region 2 slope (Neptune):   {slope2:.3f}")
print(f"Region 3 slope (gas giant): {slope3:.3f}")

# Compute chi-square
y_pred = A @ coeffs
chi_sq = np.sum((y - y_pred) ** 2)   # unweighted; divide by sigma^2 if you have errors
dof    = len(y) - len(coeffs)
print(f"\nChi-square:        {chi_sq:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"Reduced chi-square: {chi_sq / dof:.4f}")

# ── Plot ────────────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 7))
plt.scatter(data["mass"], data["radius"],
            alpha=0.3, s=5, color="steelblue", label="Planets")

# Evaluate the connected fit over each region
m1 = np.logspace(np.log10(0.01), np.log10(10),    200)
m2 = np.logspace(np.log10(10),   np.log10(100),   200)
m3 = np.logspace(np.log10(100),  np.log10(20000), 200)

def predict(m_arr):
    lx = np.log10(m_arr)
    return 10 ** (a + s1*lx + ds2*np.maximum(lx - b1, 0) + ds3*np.maximum(lx - b2, 0))

plt.plot(m1, predict(m1), color="green",  linewidth=2.5,
         label=f"Rocky    slope = {slope1:.2f}")
plt.plot(m2, predict(m2), color="orange", linewidth=2.5,
         label=f"Neptune  slope = {slope2:.2f}")
plt.plot(m3, predict(m3), color="red",    linewidth=2.5,
         label=f"Gas Giant slope = {slope3:.2f}")

# Mark the breakpoints
for bp in [10, 100]:
    plt.axvline(bp, color="gray", linestyle="--", linewidth=1, alpha=0.6)

plt.xscale("log")
plt.yscale("log")
plt.title("Planet Mass vs Radius — Connected Piecewise Fit (min. chi-square)")
plt.xlabel("Planet Mass (Earth masses)")
plt.ylabel("Planet Radius (Earth radii)")
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()