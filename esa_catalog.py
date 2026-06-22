import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Step 1 - Load ESA catalog
esa = pd.read_csv("esa_exoplanets.csv")
print("Total ESA rows:", len(esa))

# Step 2 - Rename ESA 'name' to 'pl_name'
esa = esa.rename(columns={"name": "pl_name"})

# Step 3 - Deduplicate ESA
esa = esa.drop_duplicates(subset="pl_name")
print("ESA after dedup:", len(esa))

# Step 4 - Select and rename ESA columns (same structure as unified catalog)
esa_select = esa[[
    "pl_name", "radius", "mass", "orbital_period",
    "eccentricity", "star_name", "star_mass", "star_radius",
    "star_teff", "star_distance", "ra", "dec",
    "discovered", "detection_type"
]]

# ESA doesn't have eq_temperature, add it as empty
esa_select = esa_select.copy()
esa_select["eq_temperature"] = None

# Step 5 - Normalize planet names
esa_select["pl_name"] = esa_select["pl_name"].str.strip().str.lower()

print("ESA catalog shape:", esa_select.shape)

# Step 6 - Save
esa_select.to_csv("esa_catalog.csv", index=False)
print("Saved esa_catalog.csv!")