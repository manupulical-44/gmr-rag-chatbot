import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="GMR Real Estate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    status: str = "success"


def generate_answer(question: str, history: list[dict[str, str]]) -> str:
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured on the server.",
        )

    history_text = "\n".join(f"{item.get('role', 'user')}: {item.get('content', '')}" for item in history[-10:])

    prompt = f"""
You are a professional Real Estate AI Assistant.

Answer clearly and professionally using the user's real-estate intent.
Do not invent property details or prices.
If the user asks for something unavailable, say you cannot confirm it from the current assistant setup.

Conversation History:
{history_text}

User Question:
{question}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
    except (APIConnectionError, APIStatusError, RateLimitError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Groq request failed: {exc.__class__.__name__}",
        ) from exc

    return response.choices[0].message.content


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "groq_configured": str(bool(client)).lower()}


@app.get("/")
@app.get("/api")
def root() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "GMR Real Estate API is running.",
        "health": "/api/health",
        "chat": "/api/chat",
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    reply = generate_answer(message, payload.history)

    return ChatResponse(reply=reply, status="success")
