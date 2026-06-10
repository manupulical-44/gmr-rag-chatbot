from groq import Groq
from dotenv import load_dotenv
import numpy as np
import os
import streamlit as st
import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer

# ---------------------------
# STREAMLIT CONFIG
# ---------------------------

st.set_page_config(
    page_title="Real Estate AI Assistant",
    page_icon="🏠",
    layout="centered"
)

# ---------------------------
# LOAD ENV
# ---------------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------
# SESSION MEMORY
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# LOAD MODEL
# ---------------------------

@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

# ---------------------------
# LOAD FAISS INDEX
# ---------------------------

@st.cache_resource
def load_faiss_index():

    return faiss.read_index(
        "faiss_index/property_index.faiss"
    )

# ---------------------------
# LOAD PROPERTY DATA
# ---------------------------

@st.cache_data
def load_property_data():

    return pd.read_csv(
        "database/property_data_sample.csv"
    )

# ---------------------------
# GENERATE ANSWER
# ---------------------------

def generate_answer(
    context,
    question,
    chat_history
):

    prompt = f"""
You are a professional Real Estate AI Assistant.

Your job is to help users find properties.

Rules:

1. Use ONLY the information provided in Context.
2. Never make up information.
3. Be professional and helpful.
4. If information is unavailable, say:

"I could not find that information in the property database."

5. Use Conversation History when needed.

Conversation History:
{chat_history}

Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content

# ---------------------------
# LOAD RESOURCES
# ---------------------------

model = load_model()

index = load_faiss_index()

property_df = load_property_data()

# ---------------------------
# UI
# ---------------------------

st.title("🏠 Real Estate AI Assistant")

st.caption(
    "Search properties using natural language."
)

# ---------------------------
# DISPLAY CHAT HISTORY
# ---------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# ---------------------------
# USER INPUT
# ---------------------------

question = st.chat_input(
    "Ask about properties..."
)

if question:

    # Store User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    # ---------------------------
    # EMBED QUERY
    # ---------------------------

    query_embedding = model.encode(
        [question]
    ).astype("float32")

    # ---------------------------
    # FAISS SEARCH
    # ---------------------------

    distances, indices = index.search(
        query_embedding,
        k=5
    )

    # ---------------------------
    # BUILD CONTEXT
    # ---------------------------

    context = ""

    for idx in indices[0]:

        context += (
            property_df.iloc[idx]["description"]
            + "\n\n"
        )

    # ---------------------------
    # CHAT HISTORY
    # ---------------------------

    history = []

    for msg in st.session_state.messages[-10:]:

        history.append(
            f"{msg['role']}: {msg['content']}"
        )

    chat_history = "\n".join(history)

    # ---------------------------
    # GENERATE RESPONSE
    # ---------------------------

    with st.spinner(
        "Searching properties..."
    ):

        answer = generate_answer(
            context=context,
            question=question,
            chat_history=chat_history
        )

    # ---------------------------
    # DISPLAY ANSWER
    # ---------------------------

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )