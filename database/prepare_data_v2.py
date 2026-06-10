import pandas as pd
import os

print("Loading dataset...")

df = pd.read_csv("data/realtor-data.csv")

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

df = df.dropna()

records = []

for idx, row in df.iterrows():

    description = f"""
Property available for {row['status']} in {row['city']}, {row['state']}.

Price: ${int(row['price'])}

Bedrooms: {int(row['bed'])}

Bathrooms: {int(row['bath'])}

House Size: {int(row['house_size'])} sqft

Lot Size: {row['acre_lot']} acres

Zip Code: {int(row['zip_code'])}
""".strip()

    records.append({
        "property_id": idx,
        "description": description,
        "price": row["price"],
        "bed": row["bed"],
        "bath": row["bath"],
        "city": row["city"],
        "state": row["state"],
        "house_size": row["house_size"],
        "acre_lot": row["acre_lot"],
        "status": row["status"]
    })

output_df = pd.DataFrame(records)

os.makedirs("database", exist_ok=True)

output_df.to_csv(
    "database/property_data.csv",
    index=False
)

print("Done!")
print("Rows:", len(output_df))