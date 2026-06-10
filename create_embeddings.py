import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading sample dataset...")

df = pd.read_csv(
    "database/property_data_sample.csv"
)

documents = df["description"].tolist()

print(f"Loaded {len(documents)} documents")

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    batch_size=32,
    show_progress_bar=True
)

np.save(
    "database/property_embeddings_sample.npy",
    embeddings
)

print("Embeddings saved!")
print("Shape:", embeddings.shape)