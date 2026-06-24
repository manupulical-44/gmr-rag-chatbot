"""
build_full_index.py
--------------------
Builds embeddings and a FAISS index for the FULL realtor-data.csv dataset.

Pipeline:
    data/realtor-data.csv
        -> clean + build descriptions
    database/property_data_full.csv
        -> embed in chunks of CHUNK_SIZE rows
    database/property_embeddings_full.npy
        -> build FAISS IndexFlatL2
    faiss_index/property_index_full.faiss

Existing sample-based files are NOT touched.

Once complete, retrieval.py and app_faiss.py will automatically switch
to the full index on next startup — no config change needed.

Usage:
    python build_full_index.py

Optional environment variables:
    CHUNK_SIZE   rows to embed per batch   (default 50000)
    MAX_ROWS     cap total rows for testing (default 0 = no cap)

Example test run with 100k rows:
    set MAX_ROWS=100000 && python build_full_index.py
"""

import os
import time

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 50_000))
MAX_ROWS   = int(os.getenv("MAX_ROWS",   0))        # 0 = no cap
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 256                                     # sentences per encode call

RAW_CSV   = "data/realtor-data.csv"
OUT_CSV   = "database/property_data_full.csv"
OUT_EMB   = "database/property_embeddings_full.npy"
OUT_FAISS = "faiss_index/property_index_full.faiss"

KEEP_COLS = [
    "status", "price", "bed", "bath",
    "acre_lot", "city", "state", "zip_code",
    "house_size", "prev_sold_date",
]
REQUIRED_COLS = [
    "status", "price", "bed", "bath",
    "acre_lot", "city", "state", "zip_code", "house_size",
]

os.makedirs("database",    exist_ok=True)
os.makedirs("faiss_index", exist_ok=True)


# ---------------------------------------------------------------------------
# DESCRIPTION BUILDER
# ---------------------------------------------------------------------------

def build_description(row: pd.Series) -> str:
    parts = [
        f"Property available for {row['status']} in {row['city']}, {row['state']}.",
        f"Price: ${int(row['price']):,}",
        f"Bedrooms: {int(row['bed'])}",
        f"Bathrooms: {int(row['bath'])}",
        f"House Size: {int(row['house_size'])} sqft",
        f"Lot Size: {row['acre_lot']} acres",
        f"Zip Code: {int(row['zip_code'])}",
    ]
    if pd.notna(row.get("prev_sold_date")):
        parts.append(f"Previously sold: {row['prev_sold_date']}")
    return "  ".join(parts)


# ---------------------------------------------------------------------------
# STEP 1 — LOAD & CLEAN
# ---------------------------------------------------------------------------

print("=" * 60)
print("Step 1/3  Loading and cleaning realtor-data.csv ...")
t0 = time.time()

df = pd.read_csv(RAW_CSV, low_memory=False)

# Drop rows missing required fields
df = df.dropna(subset=REQUIRED_COLS)

# Cast numerics safely
for col in ["price", "bed", "bath", "house_size", "zip_code"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["price", "bed", "bath", "house_size", "zip_code"])

# Remove nonsensical values
df = df[(df["price"] > 0) & (df["bed"] > 0) & (df["house_size"] > 0)]

if MAX_ROWS > 0:
    df = df.head(MAX_ROWS)
    print(f"  MAX_ROWS cap applied: {MAX_ROWS:,}")

df = df.reset_index(drop=True)
df["property_id"] = df.index

print(f"  Clean rows : {len(df):,}")
print(f"  Elapsed    : {time.time() - t0:.1f}s")


# ---------------------------------------------------------------------------
# STEP 2 — BUILD DESCRIPTIONS & SAVE CSV
# ---------------------------------------------------------------------------

print()
print("Step 2/3  Building descriptions and saving CSV ...")
t1 = time.time()

df["description"] = df.apply(build_description, axis=1)

out_cols = [
    "property_id", "description",
    "price", "bed", "bath", "city", "state",
    "house_size", "acre_lot", "status", "zip_code", "prev_sold_date",
]
df[out_cols].to_csv(OUT_CSV, index=False)

print(f"  Saved : {OUT_CSV}")
print(f"  Rows  : {len(df):,}")
print(f"  Elapsed: {time.time() - t1:.1f}s")


# ---------------------------------------------------------------------------
# STEP 3 — EMBED IN CHUNKS & BUILD FAISS
# ---------------------------------------------------------------------------

print()
print(f"Step 3/3  Embedding descriptions ...")
print(f"  Model      : {MODEL_NAME}")
print(f"  Chunk size : {CHUNK_SIZE:,}  |  Batch size: {BATCH_SIZE}")
t2 = time.time()

model        = SentenceTransformer(MODEL_NAME)
descriptions = df["description"].tolist()
total        = len(descriptions)
all_embeddings: list[np.ndarray] = []

for start in range(0, total, CHUNK_SIZE):
    end   = min(start + CHUNK_SIZE, total)
    chunk = descriptions[start:end]
    pct   = (end / total) * 100

    chunk_t = time.time()
    emb = model.encode(
        chunk,
        batch_size=BATCH_SIZE,
        show_progress_bar=False,
        convert_to_numpy=True,
    ).astype("float32")
    all_embeddings.append(emb)

    elapsed   = time.time() - chunk_t
    total_el  = time.time() - t2
    remaining = ((total_el / end) * (total - end)) if end > 0 else 0

    print(
        f"  [{end:>8,} / {total:,}]  {pct:5.1f}%  "
        f"chunk {elapsed:5.1f}s  ETA {remaining / 60:.1f} min"
    )

print("  Concatenating embeddings ...")
embeddings = np.vstack(all_embeddings)
np.save(OUT_EMB, embeddings)
print(f"  Saved : {OUT_EMB}  shape={embeddings.shape}")

# Build FAISS index
print("  Building FAISS IndexFlatL2 ...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(index, OUT_FAISS)
print(f"  Saved : {OUT_FAISS}  vectors={index.ntotal:,}")


# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------

total_time = time.time() - t0
print()
print("=" * 60)
print("Build complete!")
print(f"  CSV rows    : {len(df):,}")
print(f"  Embeddings  : {embeddings.shape}")
print(f"  FAISS vecs  : {index.ntotal:,}")
print(f"  Total time  : {total_time / 60:.1f} min")
print("=" * 60)
print()
print("Next steps:")
print("  Both app_faiss.py and api_server.py will automatically")
print("  switch to the full index on next startup.")
print()
print("  Run Streamlit : streamlit run app_faiss.py")
print("  Run API       : uvicorn api_server:app --host 0.0.0.0 --port 8000")
