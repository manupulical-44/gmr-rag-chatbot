import os
from typing import Any

import faiss
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

app = FastAPI(title="GMR Real Estate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = Field(default_factory=list)
    status: str = "success"


def load_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")


def load_index() -> faiss.Index:
    return faiss.read_index("faiss_index/property_index.faiss")


def load_data() -> pd.DataFrame:
    return pd.read_csv("database/property_data_sample.csv")


MODEL = load_model()
INDEX = load_index()
PROPERTY_DF = load_data()


def build_context(question: str, top_k: int = 5) -> list[str]:
    query_embedding = MODEL.encode([question]).astype("float32")
    _, indices = INDEX.search(query_embedding, k=top_k)

    descriptions: list[str] = []
    for idx in indices[0]:
        if idx < 0 or idx >= len(PROPERTY_DF):
            continue
        row = PROPERTY_DF.iloc[idx]
        descriptions.append(str(row.get("description", "")))

    return descriptions


def generate_answer(question: str, history: list[dict[str, str]], context: list[str]) -> str:
    history_text = "\n".join(f"{item.get('role', 'user')}: {item.get('content', '')}" for item in history[-10:])
    context_text = "\n\n".join(context)

    prompt = f"""
You are a professional Real Estate AI Assistant.

Use only the Context to answer the user.
If the context does not contain the answer, say you could not find that information in the property database.

Conversation History:
{history_text}

Context:
{context_text}

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    context = build_context(message)
    reply = generate_answer(message, payload.history, context)

    return ChatResponse(reply=reply, sources=context[:3], status="success")
