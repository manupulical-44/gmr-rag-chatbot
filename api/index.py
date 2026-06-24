"""
api/index.py
------------
GMR Real Estate AI — FastAPI + Groq backend.
Single file. No database. No FAISS. No local ML.

Endpoints:
    GET  /api/health
    POST /api/chat
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq, APIConnectionError, APIStatusError, RateLimitError
from pydantic import BaseModel, Field

load_dotenv()

# ---------------------------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are GMR AI, a professional real estate assistant.

You help users with:
- Finding properties by location, budget, bedrooms, and size
- Understanding property prices and market trends
- Explaining home buying, selling, and renting processes
- EMI calculations and home loan guidance
- Property documentation and legal requirements
- Neighbourhood and locality information

Rules:
1. Only answer real estate related questions.
2. If a question is not related to real estate, politely say:
   "I'm a real estate assistant and can only help with property-related questions."
3. Be concise, professional, and helpful.
4. When asked about specific properties or prices, give realistic guidance
   based on general market knowledge.
5. Always encourage users to consult a licensed agent for final decisions.
"""

# ---------------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------------

app = FastAPI(title="GMR Real Estate API", version="1.0.0")

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


class ChatResponse(BaseModel):
    reply:  str
    status: str = "success"

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "groq_configured": bool(_groq),
    }


@app.get("/")
@app.get("/api")
def root():
    return {"status": "ok", "message": "GMR Real Estate API"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    if not _groq:
        raise HTTPException(status_code=503, detail="GROQ_API_KEY is not configured.")

    # Build message list: system prompt + history + new message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in payload.history[-10:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": payload.message.strip()})

    try:
        resp = _groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=600,
        )
    except (APIConnectionError, APIStatusError, RateLimitError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Groq error: {exc.__class__.__name__}",
        ) from exc

    return ChatResponse(reply=resp.choices[0].message.content)
