import pandas as pd
import os

os.chdir(r"/home/aniket/exoplanets_project")

# Load the unified catalog
merged = pd.read_csv("exoplanets_G_type.csv", low_memory=False)

# Filter for orbital period < 100 days
short_period = merged[merged["orbital_period"] < 50]

print(f"Total planets:             {len(merged)}")
print(f"Short period planets:      {len(short_period)}")

# Save as new catalog
short_period.to_csv("short_period_exoplanets_G.csv", index=False)
print("Saved: short_period_exoplanets_G.csv")