import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the unified catalog
merged = pd.read_csv("unified_exoplanets.csv", low_memory=False)

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
print("this is graph 1")
plt.show()



# Graph 2 - Planet Mass vs Radius
plt.scatter(merged["mass"], merged["radius"],
            alpha=0.3, s=5, color="steelblue")
plt.xscale("log")
plt.yscale("log")
plt.title("Planet Mass vs Radius (Log Scale)")
plt.xlabel("Planet Mass (Earth masses)")
plt.ylabel("Planet Radius (Earth radii)")
print("this is graph 2")
plt.show()



# Graph 3 - Orbital Period Distribution
filtered_orb = merged[(merged["orbital_period"] >= 0.1) & (merged["orbital_period"] <= 1000)]
bins_orb = np.logspace(np.log10(0.1), np.log10(1000), 50)
plt.hist(filtered_orb["orbital_period"].dropna(), bins=bins_orb, color="green", edgecolor="white")
plt.xscale("log")
plt.title("Orbital Period Distribution")
plt.xlabel("Orbital Period (days)")
plt.ylabel("Number of Planets")
plt.axvline(x=365, color="red", linestyle="--", label="1 Earth year")
plt.legend()
print("this is graph 3")
plt.show()


# Graph 4 - Planet Temperature Distribution
plt.hist(merged["eq_temperature"].dropna(), bins=50, color="tomato", edgecolor="white")
plt.title("Planet Temperature Distribution")
plt.xlabel("Equilibrium Temperature (K)")
plt.ylabel("Number of Planets")
plt.axvline(x=273, color="blue", linestyle="--", label="0°C (freezing)")
plt.axvline(x=373, color="red",  linestyle="--", label="100°C (boiling)")
plt.legend()
print("this is graph 4")
plt.show()


# Graph 5 - Discovery Methods
method_counts = merged["detection_type"].value_counts()
plt.figure(figsize=(10, 6))
plt.bar(method_counts.index, method_counts.values, color="steelblue")
plt.xticks(rotation=45, ha="right")
plt.title("Planets by Discovery Method")
plt.xlabel("Method")
plt.ylabel("Number of Planets")
plt.tight_layout()
print("this is graph 5")
plt.show()


# Graph 6 - Discoveries Over Time
filtered_yr = merged[(merged["discovered"] >= 1990) & (merged["discovered"] <= 2026)]

bins_yr = range(1990, 2027, 1)
plt.figure(figsize=(12, 6))
plt.hist(filtered_yr["discovered"].dropna(), bins=bins_yr, color="steelblue", edgecolor="white")
plt.title("Exoplanet Discoveries Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Planets Discovered")
plt.xticks(range(1990, 2027, 2), rotation=45)
plt.tight_layout()
print("this is graph 6")
plt.show()
