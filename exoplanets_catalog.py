import pandas as pd
import os
from astropy.coordinates import SkyCoord
import astropy.units as u

os.chdir(r"c:\Work\Python Project")

# Step 1 - Load both catalogs
nasa = pd.read_csv("nasa_exoplanets.csv", comment='#', low_memory=False)
esa  = pd.read_csv("esa_exoplanets.csv")

# Step 2 - Drop planets with missing coordinates
nasa_clean = nasa.dropna(subset=["ra", "dec"])
esa_clean  = esa.dropna(subset=["ra", "dec"])

print("NASA rows with coordinates:", len(nasa_clean))
print("ESA rows with coordinates: ", len(esa_clean))

# Step 3 - Cross match by coordinates
nasa_coords = SkyCoord(ra=nasa_clean["ra"].values * u.degree,
                       dec=nasa_clean["dec"].values * u.degree)
esa_coords  = SkyCoord(ra=esa_clean["ra"].values * u.degree,
                       dec=esa_clean["dec"].values * u.degree)

idx, sep, _ = esa_coords.match_to_catalog_sky(nasa_coords)
match_mask = sep < 1 * u.arcsec

print("ESA planets also in NASA:", match_mask.sum())
print("ESA planets NOT in NASA: ", (~match_mask).sum())

# Step 4 - Keep only ESA planets NOT already in NASA
esa_only = esa_clean[~match_mask]

# Step 5 - Rename and normalize for merging
esa_only = esa_only.rename(columns={"name": "pl_name"})
nasa["pl_name"] = nasa["pl_name"].str.strip().str.lower()
esa_only["pl_name"] = esa_only["pl_name"].str.strip().str.lower()

# Step 6 - Combine NASA + unique ESA planets
final = pd.concat([nasa, esa_only], ignore_index=True)
print("Rows in Final catalog:", len(final))

# Step 7 - Drop duplicates and save
final_unique = final.drop_duplicates(subset="pl_name")
print("Unique planets:", len(final_unique))

final_unique.to_csv("unique_exoplanets.csv", index=False)
print("Saved!")