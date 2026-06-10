import pandas as pd
import os

# Load dataset
df = pd.read_csv("data/realtor-data.csv")

# Keep useful columns
columns = [
    "status",
    "price",
    "bed",
    "bath",
    "acre_lot",
    "city",
    "state",
    "zip_code",
    "house_size"
]

df = df[columns]

# Remove rows with missing values
df = df.dropna()

descriptions = []

for _, row in df.iterrows():

    description = f"""
Property available for {row['status']} in {row['city']}, {row['state']}.

Price: ${row['price']}

Bedrooms: {row['bed']}

Bathrooms: {row['bath']}

House Size: {row['house_size']} sqft

Lot Size: {row['acre_lot']} acres

Zip Code: {row['zip_code']}
"""

    descriptions.append(description.strip())

# Create dataframe
property_docs = pd.DataFrame({
    "description": descriptions
})

# Save
os.makedirs("database", exist_ok=True)

property_docs.to_csv(
    "database/property_descriptions.csv",
    index=False
)

print(f"Generated {len(property_docs)} property descriptions")