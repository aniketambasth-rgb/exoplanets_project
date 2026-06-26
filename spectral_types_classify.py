import pandas as pd
import os

os.chdir(r"/home/aniket/exoplanets_project")

# Load the updated catalog
final_unique = pd.read_csv("unified_exoplanets_with_spectral.csv")

# Filter and save for each spectral type
spectral_types = ["O", "B", "A", "F", "G", "K", "M"]

for sp in spectral_types:
    filtered = final_unique[
        final_unique["star_spectype"].str.startswith(sp, na=False)
    ]
    filename = f"exoplanets_{sp}_type.csv"
    filtered.to_csv(filename, index=False)
    print(f"{sp} type: {len(filtered)} planets saved to {filename}")