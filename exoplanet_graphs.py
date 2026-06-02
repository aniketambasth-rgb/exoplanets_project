import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(r"c:\Work\Python Project")

# Load the already merged file — no need to merge again!
merged = pd.read_csv("unique_exoplanets.csv", low_memory=False)

# Plot
plt.scatter(merged["pl_masse"], merged["pl_rade"],
            alpha=0.8, s=5, color="steelblue")
plt.xscale("log")
plt.yscale("log")
plt.title("Planet Mass vs Radius (Log Scale)")
plt.xlabel("Planet Mass (Earth masses)")
plt.ylabel("Planet Radius (Earth radii)")
plt.show()

plt.hist(merged["disc_year"].dropna(), bins=30, color="steelblue", edgecolor="white")
plt.title("Exoplanet Discoveries Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Planets")
plt.show()

method_counts = merged["discoverymethod"].value_counts()
plt.bar(method_counts.index, method_counts.values, color="steelblue")
plt.xticks(rotation=45, ha="right")
plt.title("Planets by Discovery Method")
plt.xlabel("Method")
plt.ylabel("Number of Planets")
plt.tight_layout()
plt.show()

plt.hist(merged["pl_eqt"].dropna(), bins=50, color="tomato", edgecolor="white")
plt.title("Planet Temperature Distribution")
plt.xlabel("Equilibrium Temperature (K)")
plt.ylabel("Number of Planets")
plt.axvline(x=273, color="blue", linestyle="--", label="0°C (freezing)")
plt.axvline(x=373, color="red", linestyle="--", label="100°C (boiling)")
plt.legend()
plt.show()

import numpy as np

filtered = merged[(merged["pl_orbper"] >= 0.1) & (merged["pl_orbper"] <= 1000)]

# Create bins evenly spaced on log scale
bins = np.logspace(np.log10(0.1), np.log10(1000), 50)

plt.hist(filtered["pl_orbper"].dropna(), bins=bins, color="green", edgecolor="white")
plt.xscale("log")
plt.title("Orbital Period Distribution")
plt.xlabel("Orbital Period (days)")
plt.ylabel("Number of Planets")
plt.axvline(x=365, color="red", linestyle="--", label="1 Earth year")
plt.legend()
plt.show()

# Filter out missing and future years
filtered = merged[(merged["disc_year"] >= 1990) & (merged["disc_year"] <= 2025)]

print("Planets with discovery year:", len(filtered))

bins = range(1990, 2026, 1)  # one bin per year

plt.figure(figsize=(12, 6))
plt.hist(filtered["disc_year"].dropna(), bins=bins, color="steelblue", edgecolor="white")
plt.title("Exoplanet Discoveries Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Planets Discovered")
plt.xticks(range(1990, 2026, 2), rotation=45)  # show every 2 years on X axis
plt.tight_layout()
plt.show()