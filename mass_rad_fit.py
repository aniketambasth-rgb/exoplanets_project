import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the unified catalog
merged = pd.read_csv("unified_exoplanets.csv", low_memory=False)

# Filter out missing values
data = merged[["mass", "radius"]].dropna()
data = data[(data["mass"] > 0) & (data["radius"] > 0)]

# Define 3 regions by mass
region1 = data[(data["mass"] >= 0.01) & (data["mass"] < 10)]
region2 = data[(data["mass"] >= 10)   & (data["mass"] < 100)]
region3 = data[(data["mass"] >= 100)  & (data["mass"] <= 20000)]

# Fit a line in log space for each region
def fit_line(region):
    log_m = np.log10(region["mass"])
    log_r = np.log10(region["radius"])
    slope, intercept, r, p, se = stats.linregress(log_m, log_r)
    return slope, intercept

slope1, intercept1 = fit_line(region1)
slope2, intercept2 = fit_line(region2)
slope3, intercept3 = fit_line(region3)

print(f"Region 1 slope (rocky):     {slope1:.3f}")
print(f"Region 2 slope (Neptune):   {slope2:.3f}")
print(f"Region 3 slope (gas giant): {slope3:.3f}")

# Plot scatter
plt.figure(figsize=(12, 7))
plt.scatter(data["mass"], data["radius"],
            alpha=0.3, s=5, color="steelblue", label="Planets")

# Plot fitted lines for each region
m1 = np.logspace(np.log10(0.01), np.log10(10),    100)
m2 = np.logspace(np.log10(10),   np.log10(100),  100)
m3 = np.logspace(np.log10(100), np.log10(20000), 100)

plt.plot(m1, 10**(slope1 * np.log10(m1) + intercept1),
         color="green",  linewidth=2, label=f"Rocky slope={slope1:.2f}")
plt.plot(m2, 10**(slope2 * np.log10(m2) + intercept2),
         color="orange", linewidth=2, label=f"Neptune slope={slope2:.2f}")
plt.plot(m3, 10**(slope3 * np.log10(m3) + intercept3),
         color="red",    linewidth=2, label=f"Gas Giant slope={slope3:.2f}")

plt.xscale("log")
plt.yscale("log")
plt.title("Planet Mass vs Radius with Fitted Slopes")
plt.xlabel("Planet Mass (Earth masses)")
plt.ylabel("Planet Radius (Earth radii)")
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()