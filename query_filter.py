"""
query_filter.py
---------------
Extracts structured metadata filters from a natural language query.

Supported filters:
    city        string match
    state       string match
    bed         int exact match
    bath        int exact match
    price_max   float
    price_min   float
    size_min    float  (house_size in sqft)
    size_max    float  (house_size in sqft)
    status      for_sale / for_rent

Returns a plain dict.  Missing filters are absent from the dict.

apply_filters(df, filters) takes a DataFrame and the filter dict
and returns a filtered DataFrame with a safe fallback.
"""

import re
import pandas as pd

# ---------------------------------------------------------------------------
# STATE MAPPINGS
# ---------------------------------------------------------------------------

STATE_NAMES = {
    "alabama": "Alabama", "alaska": "Alaska", "arizona": "Arizona",
    "arkansas": "Arkansas", "california": "California", "colorado": "Colorado",
    "connecticut": "Connecticut", "delaware": "Delaware", "florida": "Florida",
    "georgia": "Georgia", "hawaii": "Hawaii", "idaho": "Idaho",
    "illinois": "Illinois", "indiana": "Indiana", "iowa": "Iowa",
    "kansas": "Kansas", "kentucky": "Kentucky", "louisiana": "Louisiana",
    "maine": "Maine", "maryland": "Maryland", "massachusetts": "Massachusetts",
    "michigan": "Michigan", "minnesota": "Minnesota", "mississippi": "Mississippi",
    "missouri": "Missouri", "montana": "Montana", "nebraska": "Nebraska",
    "nevada": "Nevada", "new hampshire": "New Hampshire", "new jersey": "New Jersey",
    "new mexico": "New Mexico", "new york": "New York",
    "north carolina": "North Carolina", "north dakota": "North Dakota",
    "ohio": "Ohio", "oklahoma": "Oklahoma", "oregon": "Oregon",
    "pennsylvania": "Pennsylvania", "rhode island": "Rhode Island",
    "south carolina": "South Carolina", "south dakota": "South Dakota",
    "tennessee": "Tennessee", "texas": "Texas", "utah": "Utah",
    "vermont": "Vermont", "virginia": "Virginia", "washington": "Washington",
    "west virginia": "West Virginia", "wisconsin": "Wisconsin",
    "wyoming": "Wyoming", "puerto rico": "Puerto Rico",
    "virgin islands": "Virgin Islands",
}

STATE_ABBR = {
    "al": "Alabama", "ak": "Alaska", "az": "Arizona", "ar": "Arkansas",
    "ca": "California", "co": "Colorado", "ct": "Connecticut", "de": "Delaware",
    "fl": "Florida", "ga": "Georgia", "hi": "Hawaii", "id": "Idaho",
    "il": "Illinois", "in": "Indiana", "ia": "Iowa", "ks": "Kansas",
    "ky": "Kentucky", "la": "Louisiana", "me": "Maine", "md": "Maryland",
    "ma": "Massachusetts", "mi": "Michigan", "mn": "Minnesota",
    "ms": "Mississippi", "mo": "Missouri", "mt": "Montana", "ne": "Nebraska",
    "nv": "Nevada", "nh": "New Hampshire", "nj": "New Jersey",
    "nm": "New Mexico", "ny": "New York", "nc": "North Carolina",
    "nd": "North Dakota", "oh": "Ohio", "ok": "Oklahoma", "or": "Oregon",
    "pa": "Pennsylvania", "ri": "Rhode Island", "sc": "South Carolina",
    "sd": "South Dakota", "tn": "Tennessee", "tx": "Texas", "ut": "Utah",
    "vt": "Vermont", "va": "Virginia", "wa": "Washington", "wv": "West Virginia",
    "wi": "Wisconsin", "wy": "Wyoming", "pr": "Puerto Rico", "vi": "Virgin Islands",
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _parse_number(text: str) -> float | None:
    """Extract the first number (with optional k/m suffix) from a string."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*([km])\b", text, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        suffix = m.group(2).lower()
        return val * 1_000 if suffix == "k" else val * 1_000_000
    m = re.search(r"\$?([\d,]+(?:\.\d+)?)", text)
    if m:
        return float(m.group(1).replace(",", ""))
    return None


# ---------------------------------------------------------------------------
# EXTRACT FILTERS
# ---------------------------------------------------------------------------

def extract_filters(query: str) -> dict:
    """
    Parse a natural language query and return a filter dict.

    Examples:
        "3 bedroom homes in Texas under $300000"
        -> {"bed": 3, "state": "Texas", "price_max": 300000.0}

        "rental apartments in Florida with 2 baths"
        -> {"state": "Florida", "bath": 2, "status": "for_rent"}

        "large homes above 2500 sqft"
        -> {"size_min": 2500.0}
    """
    q = query.lower().strip()
    filters: dict = {}

    # --- STATUS ---
    if re.search(r"\b(for[_\s]?rent|rental|renting)\b", q):
        filters["status"] = "for_rent"
    elif re.search(r"\b(for[_\s]?sale|buying|purchase)\b", q):
        filters["status"] = "for_sale"

    # --- BEDROOMS ---
    word_nums = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8,
    }
    m = re.search(
        r"(\d+|one|two|three|four|five|six|seven|eight)"
        r"\s*[-]?\s*(bed(?:room)?s?|br)\b",
        q,
    )
    if m:
        raw = m.group(1)
        filters["bed"] = word_nums.get(raw, int(raw))

    # --- BATHROOMS ---
    m = re.search(
        r"(\d+|one|two|three|four|five)"
        r"\s*[-]?\s*(bath(?:room)?s?|ba)\b",
        q,
    )
    if m:
        raw = m.group(1)
        filters["bath"] = word_nums.get(raw, int(raw))

    # --- PRICE MAX ---
    m = re.search(
        r"(?:under|less\s+than|below|max(?:imum)?|at\s+most)"
        r"[\s$]*([0-9,]+(?:\.\d+)?(?:\s*[km])?)",
        q,
    )
    if m:
        val = _parse_number(m.group(0))
        if val:
            filters["price_max"] = val

    # --- PRICE MIN ---
    # Iterate matches; skip any that are followed immediately by a sqft unit
    _sqft_unit = re.compile(r"\s*(?:sq\.?\s*ft\.?|square\s*fe?e?t|sqft)", re.IGNORECASE)
    _price_min_re = re.compile(
        r"(?:above|more\s+than|over|min(?:imum)?|at\s+least|starting\s+(?:from|at))"
        r"[\s$]*([0-9,]+(?:\.\d+)?(?:\s*[km])?)",
        re.IGNORECASE,
    )
    for pm in _price_min_re.finditer(q):
        tail = q[pm.end():]
        if not _sqft_unit.match(tail):
            val = _parse_number(pm.group(0))
            if val:
                filters["price_min"] = val
            break

    # --- HOUSE SIZE MIN ---
    m = re.search(
        r"(?:above|over|more\s+than|larger\s+than|bigger\s+than|at\s+least)"
        r"[\s]*(\d[\d,]*)"
        r"\s*(?:sq\.?\s*ft\.?|square\s*fe?e?t|sqft)",
        q,
    )
    if m:
        filters["size_min"] = float(m.group(1).replace(",", ""))

    # --- HOUSE SIZE MAX ---
    m = re.search(
        r"(?:under|less\s+than|below|at\s+most|max(?:imum)?)"
        r"[\s]*(\d[\d,]*)"
        r"\s*(?:sq\.?\s*ft\.?|square\s*fe?e?t|sqft)",
        q,
    )
    if m:
        filters["size_max"] = float(m.group(1).replace(",", ""))

    # --- STATE (full name, longest match first) ---
    for name, canonical in sorted(STATE_NAMES.items(), key=lambda x: -len(x[0])):
        if re.search(r"\b" + re.escape(name) + r"\b", q):
            filters["state"] = canonical
            break

    # --- STATE (abbreviation fallback) ---
    if "state" not in filters:
        m = re.search(r"\b([a-z]{2})\b", q)
        if m and m.group(1) in STATE_ABBR:
            filters["state"] = STATE_ABBR[m.group(1)]

    # --- CITY ---
    city_match = re.search(
        r"\bin\s+([A-Z][a-zA-Z\s]{2,25}?)(?:\s*,|\s+(?:with|under|above|below|for|and|homes|house|property|properties)|$)",
        query,
        re.IGNORECASE,
    )
    if city_match:
        candidate = city_match.group(1).strip().title()
        if candidate.lower() not in STATE_NAMES:
            filters["city"] = candidate

    return filters


# ---------------------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------------------

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Apply extracted filters to a DataFrame.

    Falls back gracefully:
    - If all filters produce zero results, tries state-only filter.
    - If state-only also produces zero results, returns the original DataFrame.
    """
    if not filters:
        return df

    result = df.copy()

    if "state" in filters:
        result = result[result["state"].str.lower() == filters["state"].lower()]

    if "city" in filters:
        result = result[result["city"].str.lower() == filters["city"].lower()]

    if "status" in filters:
        result = result[result["status"].str.lower() == filters["status"].lower()]

    if "bed" in filters:
        result = result[result["bed"] == filters["bed"]]

    if "bath" in filters:
        result = result[result["bath"] == filters["bath"]]

    if "price_max" in filters:
        result = result[result["price"] <= filters["price_max"]]

    if "price_min" in filters:
        result = result[result["price"] >= filters["price_min"]]

    if "size_min" in filters:
        result = result[result["house_size"] >= filters["size_min"]]

    if "size_max" in filters:
        result = result[result["house_size"] <= filters["size_max"]]

    # Fallback: too strict -> relax to state only
    if len(result) == 0:
        if "state" in filters:
            state_only = df[df["state"].str.lower() == filters["state"].lower()]
            if len(state_only) > 0:
                return state_only
        return df  # full fallback

    return result
