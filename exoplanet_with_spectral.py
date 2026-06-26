import pandas as pd
import os
os.chdir(r"/home/aniket/exoplanets_project")
# 1. Load the catalog
final_unique = pd.read_csv("unified_exoplanets.csv")

# 2. Define the function
def teff_to_spectral(teff):
    if pd.isna(teff):
        return None
    elif teff > 33000:
        return "O"
    elif teff > 10000:
        return "B"
    elif teff > 7300:
        return "A"
    elif teff > 6000:
        return "F"
    elif teff > 5300:
        return "G"
    elif teff > 3900:
        return "K"
    elif teff > 2300:
        return "M"
    else:
        return None

# 3. Fill missing spectral types
mask = final_unique["star_spectype"].isna()
final_unique.loc[mask, "star_spectype"] = (
    final_unique.loc[mask, "star_teff"].apply(teff_to_spectral)
)

# 4. Save the updated catalog
final_unique.to_csv("unified_exoplanets_with_spectral.csv", index=False)
print("Done!")