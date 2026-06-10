import pandas as pd
import os
from astropy.coordinates import SkyCoord
import astropy.units as u

os.chdir(r"c:\Work\Python Project")

# Step 1 - Load both catalogs
nasa = pd.read_csv("nasa_exoplanets.csv", comment='#', low_memory=False)
esa  = pd.read_csv("esa_exoplanets.csv")

# Step 2 - Rename ESA 'name' to 'pl_name'
esa = esa.rename(columns={"name": "pl_name"})

# Step 3 - Deduplicate NASA
nasa = nasa.drop_duplicates(subset="pl_name")
print("NASA after dedup:", len(nasa))

# Step 4 - Normalize names
nasa = nasa.copy()
nasa["pl_name_norm"] = nasa["pl_name"].str.strip().str.lower().str.replace(" ", "")
esa["pl_name_norm"]  = esa["pl_name"].str.strip().str.lower().str.replace(" ", "")

# Step 5 - Name matching: find ESA planets not in NASA by name
esa_not_by_name = esa[~esa["pl_name_norm"].isin(nasa["pl_name_norm"])]
print("ESA not matched by name:  ", len(esa_not_by_name))

# Step 6 - Coordinate matching on remaining ESA planets
nasa_clean = nasa.dropna(subset=["ra", "dec"])
esa_not_by_name = esa_not_by_name.dropna(subset=["ra", "dec"])

nasa_coords = SkyCoord(ra=nasa_clean["ra"].values * u.degree,
                       dec=nasa_clean["dec"].values * u.degree)
esa_coords  = SkyCoord(ra=esa_not_by_name["ra"].values * u.degree,
                       dec=esa_not_by_name["dec"].values * u.degree)

idx, sep, _ = esa_coords.match_to_catalog_sky(nasa_coords)
coord_mask  = sep < 20 * u.arcsec

esa_truly_unique = esa_not_by_name[~coord_mask]
print("ESA truly unique planets: ", len(esa_truly_unique))

# Step 7 - Select and rename NASA columns
nasa_select = nasa[[
    "pl_name", "pl_rade", "pl_bmasse", "pl_orbper",
    "pl_orbeccen", "hostname", "st_mass", "st_rad",
    "st_teff", "sy_dist", "ra", "dec",
    "disc_year", "discoverymethod"
]].rename(columns={
    "pl_rade"        : "radius",
    "pl_bmasse"       : "mass",
    "pl_orbper"      : "orbital_period",
    "pl_orbeccen"    : "eccentricity",
    "hostname"       : "star_name",
    "st_mass"        : "star_mass",
    "st_rad"         : "star_radius",
    "st_teff"        : "star_teff",
    "sy_dist"        : "star_distance",
    "disc_year"      : "discovered",
    "discoverymethod": "detection_type"
})

# Step 8 - Select ESA truly unique columns
esa_select = esa_truly_unique[[
    "pl_name", "radius", "mass", "orbital_period",
    "eccentricity", "star_name", "star_mass", "star_radius",
    "star_teff", "star_distance", "ra", "dec",
    "discovered", "detection_type"
]]

print("NASA selected shape:", nasa_select.shape)
print("ESA unique shape:   ", esa_select.shape)

# Step 9 - Combine and save
final = pd.concat([nasa_select, esa_select], ignore_index=True)
final["pl_name"] = final["pl_name"].str.strip().str.lower()
final_unique = final.drop_duplicates(subset="pl_name")

print("Final unique planets:", len(final_unique))

final_unique.to_csv("unified_exoplanets.csv", index=False)
print("Saved!")