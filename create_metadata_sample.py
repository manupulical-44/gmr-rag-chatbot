import pandas as pd

print("Loading property_data.csv...")

df = pd.read_csv(
    "database/property_data.csv"
)

sample_df = df.sample(
    n=10000,
    random_state=42
)

sample_df.to_csv(
    "database/property_data_sample.csv",
    index=False
)

print("Sample created successfully!")
print("Rows:", len(sample_df))
print("Columns:")
print(sample_df.columns)