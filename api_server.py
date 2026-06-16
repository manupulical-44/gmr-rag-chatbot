"""
api_server.py
-------------
FastAPI backend for the GMR Real Estate AI Assistant.

Endpoints
---------
GET  /api/health
POST /api/chat                       — RAG answer (FAISS + Groq)
POST /api/search                     — raw FAISS retrieval, no LLM
GET  /api/properties                 — paginated, filtered property list
GET  /api/properties/featured        — top N properties for landing page
GET  /api/properties/{property_id}   — single property record
GET  /api/properties/{property_id}/similar — related properties

All retrieval logic lives in retrieval.py — single source of truth.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq, APIConnectionError, APIStatusError, RateLimitError
from pydantic import BaseModel, Field

from retrieval import startup, retrieve, get_properties, load_dataframe

load_dotenv()

# ---------------------------------------------------------------------------
# STARTUP
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load CSV, model, and FAISS index before serving any requests.
    # On first run this builds and saves the FAISS index (~30-90 min for full CSV).
    # On subsequent runs it loads from disk (seconds).
    startup()
    yield


# ---------------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------------

app = FastAPI(
    title="GMR Real Estate API",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_groq = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None


# ---------------------------------------------------------------------------
# SCHEMAS
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[dict[str, str]] = Field(default_factory=list)
    top_k:   int = Field(default=10, ge=1, le=50)


class ChatResponse(BaseModel):
    reply:   str
    hits:    int
    filters: dict
    status:  str = "success"


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=10, ge=1, le=50)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _build_prompt(context: str, question: str, history: list[dict]) -> str:
    history_text = "\n".join(
        f"{m.get('role','user')}: {m.get('content','')}"
        for m in history[-10:]
    )
    return f"""You are a professional Real Estate AI Assistant.

Rules:
1. Use ONLY the property information in Context.
2. Never invent prices, addresses, or details.
3. Be concise and helpful.
4. If no relevant results exist, say: "I could not find matching properties. Try broadening your search."
5. Use Conversation History for follow-up questions.

Conversation History:
{history_text}

Context (retrieved properties):
{context}

User Question:
{question}

Answer:"""


def _shape_property(row: dict) -> dict:
    """Normalise a raw CSV row into the shape the React frontend expects."""
    return {
        "id":          str(row.get("property_id", "")),
        "title":       f"{_safe_int(row.get('bed'))} Bed in {row.get('city', '')}, {row.get('state', '')}",
        "price":       row.get("price", 0),
        "city":        row.get("city", ""),
        "state":       row.get("state", ""),
        "status":      row.get("status", ""),
        "bedrooms":    _safe_int(row.get("bed")),
        "bathrooms":   _safe_int(row.get("bath")),
        "area":        _safe_int(row.get("house_size")),
        "bhk":         _safe_int(row.get("bed")),
        "description": row.get("description", ""),
        "zip_code":    row.get("zip_code", ""),
        "acre_lot":    row.get("acre_lot", 0),
        "prev_sold_date": row.get("prev_sold_date"),
        # Placeholder image — replace with real images if available
        "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
        "amenities": [],
    }


def _safe_int(value) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


# ---------------------------------------------------------------------------
# ROUTES — Meta
# ---------------------------------------------------------------------------

@app.get("/")
@app.get("/api")
def root():
    return {
        "status": "ok",
        "version": "2.0.0",
        "endpoints": {
            "health":     "GET  /api/health",
            "chat":       "POST /api/chat",
            "search":     "POST /api/search",
            "properties": "GET  /api/properties",
            "featured":   "GET  /api/properties/featured",
            "detail":     "GET  /api/properties/{id}",
            "similar":    "GET  /api/properties/{id}/similar",
        },
    }


@app.get("/api/health")
def health():
    df = load_dataframe()
    return {
        "status":          "ok",
        "groq_configured": bool(_groq),
        "total_properties": len(df),
    }


# ---------------------------------------------------------------------------
# ROUTES — Chat
# ---------------------------------------------------------------------------

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    if not _groq:
        raise HTTPException(status_code=503, detail="GROQ_API_KEY is not configured.")

    message = payload.message.strip()
    result  = retrieve(message, top_k=payload.top_k, return_filters=True)
    prompt  = _build_prompt(result["context"], message, payload.history)

    try:
        resp = _groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600,
        )
    except (APIConnectionError, APIStatusError, RateLimitError) as exc:
        raise HTTPException(status_code=502, detail=f"Groq error: {exc.__class__.__name__}") from exc

    return ChatResponse(
        reply=resp.choices[0].message.content,
        hits=result["hits"],
        filters=result["filters"],
    )


@app.post("/api/search")
def search(payload: SearchRequest):
    result = retrieve(payload.query, top_k=payload.top_k, return_filters=True)
    return {
        "properties": [_shape_property(p) for p in result["properties"]],
        "hits":       result["hits"],
        "filters":    result["filters"],
    }


# ---------------------------------------------------------------------------
# ROUTES — Properties
# ---------------------------------------------------------------------------

@app.get("/api/properties")
def list_properties(
    city:      str | None = Query(default=None),
    state:     str | None = Query(default=None),
    status:    str | None = Query(default=None),
    bed:       int | None = Query(default=None),
    bath:      int | None = Query(default=None),
    bhk:       int | None = Query(default=None),        # alias for bed
    min_price: float | None = Query(default=None, alias="minPrice"),
    max_price: float | None = Query(default=None, alias="maxPrice"),
    min_size:  float | None = Query(default=None),
    query:     str | None = Query(default=None),        # text search via FAISS
    page:      int = Query(default=1, ge=1),
    page_size: int = Query(default=8, ge=1, le=100, alias="pageSize"),
):
    # If a free-text query is provided, use FAISS retrieval
    if query and query.strip():
        result = retrieve(query.strip(), top_k=page_size, return_filters=True)
        props  = [_shape_property(p) for p in result["properties"]]
        return {
            "data": props,
            "pagination": {
                "page":        page,
                "page_size":   page_size,
                "total":       result["hits"],
                "total_pages": 1,
            },
        }

    # Otherwise use structured filter query
    result = get_properties(
        city=city,
        state=state,
        bed=bed or bhk,
        bath=bath,
        price_min=min_price,
        price_max=max_price,
        size_min=min_size,
        status=status,
        page=page,
        page_size=page_size,
    )
    return {
        "data":       [_shape_property(p) for p in result["data"]],
        "pagination": result["pagination"],
    }


@app.get("/api/properties/featured")
def featured_properties(limit: int = Query(default=6, ge=1, le=20)):
    """Returns top N properties sorted by price descending for the landing page."""
    df     = load_dataframe()
    sample = df.nlargest(limit, "price")
    props  = [_shape_property(row) for row in sample.to_dict(orient="records")]
    return {"data": props}


@app.get("/api/properties/{property_id}")
def get_property(property_id: str):
    df = load_dataframe()
    try:
        idx = int(property_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found.")

    if idx < 0 or idx >= len(df):
        raise HTTPException(status_code=404, detail="Property not found.")

    row = df.iloc[idx].to_dict()
    row["property_id"] = idx
    return _shape_property(row)


@app.get("/api/properties/{property_id}/similar")
def similar_properties(property_id: str, limit: int = Query(default=4, ge=1, le=12)):
    """Find similar properties using FAISS on the description of the target property."""
    df = load_dataframe()
    try:
        idx = int(property_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found.")

    if idx < 0 or idx >= len(df):
        raise HTTPException(status_code=404, detail="Property not found.")

    description = df.iloc[idx]["description"]
    result      = retrieve(description, top_k=limit + 1)

    # Exclude the property itself from results
    props = [
        _shape_property(p)
        for p in result["properties"]
        if str(p.get("property_id", "")) != property_id
    ][:limit]

    return {"data": props}
