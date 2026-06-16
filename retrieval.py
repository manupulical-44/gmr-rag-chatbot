"""
retrieval.py
------------
Single source of truth for all retrieval logic.

Startup strategy — fast by default:
  If  faiss_index/property_index.faiss  exists (sample, 10k rows):
      Server starts in ~10 seconds. Chat and search work immediately.

  After running  python build_full_index.py:
      faiss_index/property_index_full.faiss  is created.
      On next server start it loads the full index (seconds from disk).

Data:
  The full realtor-data.csv is always loaded for structured /api/properties
  queries (filter by city/state/bed/price).  That load happens once and is
  cached.  The FAISS index is separate — it maps vector positions to row
  indices in that DataFrame.
"""

import os
from functools import lru_cache
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from query_filter import extract_filters, apply_filters

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

_FULL_FAISS   = Path("faiss_index/property_index_full.faiss")
_FULL_IDMAP   = Path("faiss_index/id_map.npy")
_SAMPLE_FAISS = Path("faiss_index/property_index.faiss")
_SAMPLE_CSV   = Path("database/property_data_sample.csv")
_FULL_CSV     = Path("data/realtor-data.csv")

MODEL_NAME    = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = int(os.getenv("TOP_K", 20))
BATCH_SIZE    = 256

REQUIRED_COLS = ["status", "price", "bed", "bath",
                 "acre_lot", "city", "state", "zip_code", "house_size"]


# ---------------------------------------------------------------------------
# DESCRIPTION BUILDER
# ---------------------------------------------------------------------------

def _build_description(row: pd.Series) -> str:
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
# SAMPLE DATA LOADER  (fast — used only when full data isn't needed)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_sample_df() -> pd.DataFrame:
    """Load the 10k sample CSV — fast, used as FAISS lookup table for sample index."""
    df = pd.read_csv(_SAMPLE_CSV)
    for col in ["price", "bed", "bath", "house_size", "acre_lot"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# ---------------------------------------------------------------------------
# FULL DATA LOADER  (slow first call, then cached)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_dataframe() -> pd.DataFrame:
    """
    Load, clean, and cache the full realtor-data.csv.
    Called on demand by /api/properties endpoints.
    Not called at startup — server starts without waiting for this.
    """
    print("[retrieval] Loading full dataset (data/realtor-data.csv) ...")
    df = pd.read_csv(_FULL_CSV, low_memory=False)

    df = df.dropna(subset=REQUIRED_COLS)
    for col in ["price", "bed", "bath", "house_size", "zip_code", "acre_lot"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["price", "bed", "bath", "house_size", "zip_code"])
    df = df[(df["price"] > 0) & (df["bed"] > 0) & (df["house_size"] > 0)]
    df = df.reset_index(drop=True)
    df["description"] = df.apply(_build_description, axis=1)

    print(f"[retrieval] Full dataset ready: {len(df):,} properties")
    return df


# ---------------------------------------------------------------------------
# EMBEDDING MODEL  (cached)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    print(f"[retrieval] Loading embedding model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)


# ---------------------------------------------------------------------------
# FAISS INDEX  (fast load from disk — build separately via build_full_index.py)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_index() -> tuple[faiss.Index, pd.DataFrame, str]:
    """
    Returns (faiss_index, lookup_df, label).
    lookup_df is the DataFrame whose row order matches the FAISS vector positions.
    label is 'full' or 'sample'.

    Priority:
      1. Full index on disk  → load it + full CSV as lookup
      2. Sample index on disk → load it + sample CSV as lookup (server ready instantly)
      3. Neither exists      → raise with clear instructions
    """
    force_rebuild = os.getenv("REBUILD_INDEX", "0") == "1"
    full_ready    = _FULL_FAISS.exists() and _FULL_IDMAP.exists()

    if full_ready and not force_rebuild:
        print("[retrieval] Loading full FAISS index from disk ...")
        index  = faiss.read_index(str(_FULL_FAISS))
        # id_map maps vector position → row in full CSV
        # We need the full df loaded for lookups
        lookup_df = load_dataframe()
        print(f"[retrieval] Full index ready: {index.ntotal:,} vectors")
        return index, lookup_df, "full"

    if _SAMPLE_FAISS.exists() and not force_rebuild:
        print("[retrieval] Full index not found — using sample index (10k rows).")
        print("[retrieval] For full dataset: run  python build_full_index.py")
        index     = faiss.read_index(str(_SAMPLE_FAISS))
        lookup_df = _load_sample_df()
        print(f"[retrieval] Sample index ready: {index.ntotal:,} vectors")
        return index, lookup_df, "sample"

    raise RuntimeError(
        "No FAISS index found.\n"
        "Run:  python build_full_index.py\n"
        "Then restart the server."
    )


# ---------------------------------------------------------------------------
# STARTUP  (called once at server startup — must be fast)
# ---------------------------------------------------------------------------

def startup() -> None:
    """
    Pre-load embedding model and FAISS index at server startup.
    Does NOT load the full CSV — that happens on first /api/properties call.
    Server is ready in ~10 seconds when sample index exists.
    """
    get_model()
    get_index()
    print("[retrieval] Startup complete. Server is ready.")


# ---------------------------------------------------------------------------
# RETRIEVE  (FAISS semantic search)
# ---------------------------------------------------------------------------

def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    return_filters: bool = False,
) -> dict:
    """
    Semantic retrieval pipeline:
      1. Parse metadata filters from query
      2. Embed query
      3. FAISS nearest-neighbour search
      4. Apply metadata filters to candidates
      5. Return context string + property records
    """
    model                   = get_model()
    index, lookup_df, label = get_index()

    # 1. Parse filters
    filters = extract_filters(query)

    # 2. Embed
    query_vec = model.encode([query]).astype("float32")

    # 3. FAISS search
    fetch_k = min(top_k * 6 if filters else top_k * 2, index.ntotal)
    _, raw_indices = index.search(query_vec, k=fetch_k)

    # 4. Map indices → rows (clamp to lookup_df length for safety)
    idx   = raw_indices[0]
    idx   = idx[idx < len(lookup_df)]
    candidates = lookup_df.iloc[idx].copy()

    # 5. Apply metadata filters
    filtered = apply_filters(candidates, filters)
    results  = filtered.head(top_k)

    context = "\n\n---\n\n".join(results["description"].tolist())

    output_cols = [c for c in
        ["property_id", "description", "status", "price", "bed", "bath",
         "city", "state", "zip_code", "house_size", "acre_lot", "prev_sold_date"]
        if c in results.columns]

    out = {
        "context"   : context,
        "properties": results[output_cols].to_dict(orient="records"),
        "hits"      : len(results),
        "label"     : label,
    }
    if return_filters:
        out["filters"] = filters
    return out


# ---------------------------------------------------------------------------
# GET PROPERTIES  (structured filter query on full CSV)
# ---------------------------------------------------------------------------

def get_properties(
    city:       str | None = None,
    state:      str | None = None,
    bed:        int | None = None,
    bath:       int | None = None,
    price_min:  float | None = None,
    price_max:  float | None = None,
    size_min:   float | None = None,
    status:     str | None = None,
    page:       int = 1,
    page_size:  int = 8,
) -> dict:
    """
    Structured property listing for /api/properties.
    Loads the full CSV on first call (cached after that).
    """
    df     = load_dataframe()
    result = df.copy()

    if state:
        result = result[result["state"].str.lower() == state.lower()]
    if city:
        result = result[result["city"].str.lower() == city.lower()]
    if status:
        result = result[result["status"].str.lower() == status.lower()]
    if bed is not None:
        result = result[result["bed"] == float(bed)]
    if bath is not None:
        result = result[result["bath"] == float(bath)]
    if price_min is not None:
        result = result[result["price"] >= price_min]
    if price_max is not None:
        result = result[result["price"] <= price_max]
    if size_min is not None:
        result = result[result["house_size"] >= size_min]

    total       = len(result)
    total_pages = max(1, -(-total // page_size))
    start       = (page - 1) * page_size
    page_rows   = result.iloc[start: start + page_size]

    output_cols = [c for c in
        ["status", "price", "bed", "bath", "city", "state",
         "zip_code", "house_size", "acre_lot", "prev_sold_date", "description"]
        if c in page_rows.columns]

    return {
        "data": page_rows[output_cols].to_dict(orient="records"),
        "pagination": {
            "page":        page,
            "page_size":   page_size,
            "total":       total,
            "total_pages": total_pages,
        },
    }
