import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Step 1 - Load NASA catalog
nasa = pd.read_csv("nasa_exoplanets.csv", comment='#', low_memory=False)
print("Total NASA rows:", len(nasa))

# Step 2 - Deduplicate NASA
nasa = nasa.drop_duplicates(subset="pl_name")
print("NASA after dedup:", len(nasa))

# Step 3 - Select and rename NASA columns (same as unified catalog)

nasa_select = nasa[[
    "pl_name", "pl_rade", "pl_bmasse", "pl_orbper",
    "pl_orbeccen", "hostname", "st_mass", "st_rad",
    "st_teff", "sy_dist", "ra", "dec",
    "disc_year", "discoverymethod", "pl_eqt",
    "disc_facility"          # ← add this
]].rename(columns={
    "pl_rade"        : "radius",
    "pl_bmasse"      : "mass",
    "pl_orbper"      : "orbital_period",
    "pl_orbeccen"    : "eccentricity",
    "hostname"       : "star_name",
    "st_mass"        : "star_mass",
    "st_rad"         : "star_radius",
    "st_teff"        : "star_teff",
    "sy_dist"        : "star_distance",
    "disc_year"      : "discovered",
    "discoverymethod": "detection_type",
    "pl_eqt"         : "eq_temperature",
    "disc_facility"  : "facility"   # ← add this
})
# Step 4 - Normalize planet names
nasa_select = nasa_select.copy()
nasa_select["pl_name"] = nasa_select["pl_name"].str.strip().str.lower()

print("NASA catalog shape:", nasa_select.shape)

# Step 5 - Save
nasa_select.to_csv("nasa_catalog.csv", index=False)
print("Saved nasa_catalog.csv!")