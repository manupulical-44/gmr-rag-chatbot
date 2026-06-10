import pandas as pd
import numpy as np

print("Loading dataset...")

df = pd.read_csv(
    "data/realtor-data.csv",
    low_memory=False
)

print(f"Original Rows: {len(df)}")

# -----------------------
# Remove Duplicates
# -----------------------

df = df.drop_duplicates()

print(f"After Duplicate Removal: {len(df)}")

# -----------------------
# Keep Required Columns
# -----------------------

required_columns = [
    "brokered_by",
    "status",
    "price",
    "bed",
    "bath",
    "acre_lot",
    "street",
    "city",
    "state",
    "zip_code",
    "house_size",
    "prev_sold_date"
]

df = df[required_columns]

# -----------------------
# Handle Missing Values
# -----------------------

df = df.dropna(
    subset=[
        "price",
        "bed",
        "bath",
        "city",
        "state"
    ]
)

# -----------------------
# Clean Text Columns
# -----------------------

text_columns = [
    "city",
    "state",
    "status"
]

for col in text_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
    )

# -----------------------
# Numeric Conversion
# -----------------------

numeric_columns = [
    "price",
    "bed",
    "bath",
    "acre_lot",
    "house_size"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# -----------------------
# Remove Invalid Values
# -----------------------

df = df[
    (df["price"] > 0)
]

df = df[
    (df["bed"] > 0)
]

df = df[
    (df["bath"] > 0)
]

# -----------------------
# Reset Index
# -----------------------

df = df.reset_index(drop=True)

# -----------------------
# Create Property ID
# -----------------------

df.insert(
    0,
    "property_id",
    range(1, len(df) + 1)
)

# -----------------------
# Save Clean Dataset
# -----------------------

output_file = (
    "database/cleaned_properties.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\nCleaning Complete")
print(f"Final Rows: {len(df)}")
print(f"Saved To: {output_file}")

print("\nColumns:")
print(df.columns.tolist())

print("\nSample:")
print(df.head())