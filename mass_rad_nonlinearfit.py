import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
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

# ── Core function: given breakpoints, solve for best linear coeffs ──────────
def fit_given_breakpoints(b1, b2):
    """Build design matrix and solve least squares for fixed b1, b2."""
    A = np.column_stack([
        np.ones_like(x),
        x,
        np.maximum(x - b1, 0),
        np.maximum(x - b2, 0),
    ])
    coeffs, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    y_pred = A @ coeffs
    chi_sq = np.sum((y - y_pred) ** 2)
    return chi_sq, coeffs

# ── Objective: only exposes breakpoints to the optimizer ────────────────────
def objective(params):
    b1, b2 = params
    # Keep b1 < b2 and within data range, else penalize
    if b1 >= b2 or b1 < np.log10(0.1) or b2 > np.log10(10000):
        return 1e10
    chi_sq, _ = fit_given_breakpoints(b1, b2)
    return chi_sq

# ── Optimize breakpoints starting from our fixed guesses ────────────────────
b1_init = np.log10(10)    # start at 10  Earth masses
b2_init = np.log10(100)   # start at 100 Earth masses

result = minimize(
    objective,
    x0=[b1_init, b2_init],
    method="Nelder-Mead",          # derivative-free, robust for this problem
    options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 10000}
)

b1_opt, b2_opt = result.x
bp1_opt = 10 ** b1_opt    # back to Earth masses
bp2_opt = 10 ** b2_opt

chi_sq_opt, coeffs_opt = fit_given_breakpoints(b1_opt, b2_opt)
a, s1, ds2, ds3 = coeffs_opt

slope1 = s1
slope2 = s1 + ds2
slope3 = s1 + ds2 + ds3

dof = len(y) - 4    # 4 parameters: a, s1, ds2, ds3

print(f"Optimized breakpoint 1: {bp1_opt:.2f} Earth masses  (was 10)")
print(f"Optimized breakpoint 2: {bp2_opt:.2f} Earth masses  (was 100)")
print(f"\nRegion 1 slope (rocky):     {slope1:.3f}")
print(f"Region 2 slope (Neptune):   {slope2:.3f}")
print(f"Region 3 slope (gas giant): {slope3:.3f}")
print(f"\nChi-square:         {chi_sq_opt:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"Reduced chi-square: {chi_sq_opt / dof:.4f}")

# Compare with fixed breakpoints
chi_sq_fixed, _ = fit_given_breakpoints(b1_init, b2_init)
print(f"\nChi-square improvement over fixed breakpoints: {chi_sq_fixed - chi_sq_opt:.4f}")

# ── Plot ─────────────────────────────────────────────────────────────────────
def predict(m_arr):
    lx = np.log10(m_arr)
    return 10 ** (a + s1*lx + ds2*np.maximum(lx - b1_opt, 0)
                             + ds3*np.maximum(lx - b2_opt, 0))

plt.figure(figsize=(12, 7))
plt.scatter(data["mass"], data["radius"],
            alpha=0.3, s=5, color="steelblue", label="Planets")

m1 = np.logspace(np.log10(0.01),   b1_opt,          200)
m2 = np.logspace(b1_opt,           b2_opt,          200)
m3 = np.logspace(b2_opt,           np.log10(20000), 200)

plt.plot(m1, predict(m1), color="green",  linewidth=2.5,
         label=f"Rocky     slope = {slope1:.2f}")
plt.plot(m2, predict(m2), color="orange", linewidth=2.5,
         label=f"Neptune   slope = {slope2:.2f}")
plt.plot(m3, predict(m3), color="red",    linewidth=2.5,
         label=f"Gas Giant slope = {slope3:.2f}")

# Mark optimized breakpoints
for bp, label in [(bp1_opt, f"BP1 = {bp1_opt:.1f} M⊕"),
                  (bp2_opt, f"BP2 = {bp2_opt:.1f} M⊕")]:
    plt.axvline(bp, color="gray", linestyle="--", linewidth=1.2, alpha=0.7)
    plt.text(bp * 1.05, plt.ylim()[0] * 1.3, label,
             fontsize=9, color="gray", va="bottom")

plt.xscale("log")
plt.yscale("log")
plt.title("Planet Mass vs Radius — Optimized Piecewise Fit (min. chi-square)")
plt.xlabel("Planet Mass (Earth masses)")
plt.ylabel("Planet Radius (Earth radii)")
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()