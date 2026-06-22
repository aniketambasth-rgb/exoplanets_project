import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the nasa catalog 
merged = pd.read_csv("nasa_catalog.csv", low_memory=False)

kepler_only = merged[merged["facility"] == "Kepler"]
print("Kepler planets:", len(kepler_only))

print(merged["facility"].value_counts().head(20))
print("\nKepler planets found:", len(merged[merged["facility"] == "Kepler"]))



kepler_short_period = kepler_only[kepler_only["orbital_period"] < 100]
print("Short-period Kepler planets:", len(kepler_short_period))

bins_log = np.logspace(np.log10(0.5), np.log10(4), 60)
plt.figure(figsize=(12, 6))
plt.hist(kepler_short_period["radius"].dropna(), bins=bins_log, color="steelblue", edgecolor="white")
plt.xscale("log")
plt.xlim(0.5, 4)
plt.title("Planet Radius Distribution (Kepler, P < 100 days)")
plt.xlabel("Planet Radius (Earth radii)")
plt.ylabel("Number of Planets")
plt.show()