import pandas as pd
import os

os.chdir(r"c:\Work\Python Project")

nasa = pd.read_csv("nasa_exoplanets.csv", comment='#', low_memory=False)
esa  = pd.read_csv("esa_exoplanets.csv")

# Step 1 - Rename ESA's 'name' to match NASA's 'pl_name'
esa = esa.rename(columns={"name": "pl_name"})

# Step 2 - Normalize planet names (strip spaces, lowercase)
nasa["pl_name"] = nasa["pl_name"].str.strip().str.lower()
esa["pl_name"]  = esa["pl_name"].str.strip().str.lower()

# Step 3 - Merge (keeping all planets from both)
merged = pd.merge(nasa, esa, on="pl_name", how="outer", suffixes=("_nasa", "_esa"))

# Step 4 - Check result
print("Merged shape:", merged.shape)

# Step 5 - Save
merged.to_csv("merged_exoplanets.csv", index=False)
print("Saved successfully!")

# Keep only one row per planet
merged_unique = merged.drop_duplicates(subset="pl_name")

print("Total rows in merged:  ", len(merged))
print("Unique planets:        ", len(merged_unique))

# Save as a new CSV
merged_unique.to_csv("unique_exoplanets.csv", index=False)
print("Saved successfully!")

print("Rows in unique file:", len(merged_unique))
# Should print 8136

# Read the saved file back and check
verify = pd.read_csv("unique_exoplanets.csv", low_memory=False)
print("Rows in saved file:", len(verify))