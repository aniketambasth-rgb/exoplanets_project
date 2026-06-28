import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the unified catalog
merged = pd.read_csv("short_period_exoplanets_G.csv", low_memory=False)

# Graph 1 - Planet Size Distribution with Planet Types and Radius Valley
bins_size = np.arange(0.5, 12.1, 0.1)

plt.figure(figsize=(14, 6))
plt.hist(merged["radius"].dropna(), bins=bins_size, color="steelblue", edgecolor="white")

# Add shaded regions for each planet type
plt.axvspan(0.5,  1.25, alpha=0.15, color="green",  label="Earth-size")
plt.axvspan(1.25, 2.0,  alpha=0.15, color="orange", label="Super-Earth")
plt.axvspan(2.0,  4.0,  alpha=0.15, color="red",    label="Sub-Neptune")
plt.axvspan(4.0,  10.0, alpha=0.15, color="purple",  label="Neptune-like")
plt.axvspan(10.0, 12.0, alpha=0.15, color="brown",  label="Gas Giant")

# Add vertical lines for planet type boundaries
plt.axvline(x=1.25, color="green",  linestyle="--", linewidth=1.5)
plt.axvline(x=4.0,  color="red",    linestyle="--", linewidth=1.5)
plt.axvline(x=10.0, color="purple", linestyle="--", linewidth=1.5)

# Highlight the radius valley ON TOP of everything
plt.axvspan(1.5, 2.0, alpha=0.5, color="gray", label="Radius Valley (Fulton Gap)")
plt.axvline(x=1.5, color="black", linestyle="-", linewidth=2)
plt.axvline(x=2.0, color="black", linestyle="-", linewidth=2)

# Add planet type labels on top of graph
plt.text(0.85, 155, "Earth",       fontsize=8, color="green",  rotation=90)
plt.text(1.30, 155, "Super-Earth", fontsize=8, color="orange", rotation=90)
plt.text(2.10, 155, "Sub-Neptune", fontsize=8, color="red",    rotation=90)
plt.text(5.00, 155, "Neptune-like",fontsize=8, color="purple", rotation=90)
plt.text(10.2, 155, "Gas Giant",   fontsize=8, color="brown",  rotation=90)

plt.title("Distribution of Planet Sizes by Type (with Radius Valley)")
plt.xlabel("Planet Radius (Earth radii)")
plt.ylabel("Number of Planets")
plt.xlim(0.5, 12)
plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.show()

