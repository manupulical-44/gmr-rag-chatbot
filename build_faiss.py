import numpy as np
import faiss

print("Loading embeddings...")

embeddings = np.load(
    "database/property_embeddings_sample.npy"
).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(embeddings)

faiss.write_index(
    index,
    "faiss_index/property_index.faiss"
)

print("Index created successfully!")
print("Total vectors:", index.ntotal)