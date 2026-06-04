
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(context, question):

    prompt = f"""
You are a GMR Real Estate Assistant.

Use ONLY the information provided in the context.

Rules:
1. Do NOT perform calculations unless the user explicitly asks.
2. Do NOT combine information from different context sections.
3. Give short and direct answers.
4. If the answer exists in the context, repeat it exactly.
5. If the answer does not exist, reply exactly:
I could not find that information in the available data.

Context:
{context}

Question:
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
        ]
    )

    return response.choices[0].message.content

st.set_page_config(
    page_title="GMR Real Estate Chatbot",
    page_icon="🏢"

)    
documents = []

files = [
    "data/flats.txt",
    "data/terms.txt",
    "data/emi.txt"
]

for file_name in files:
    with open(file_name, "r", encoding="utf-8") as file:
        documents.append(file.read())

st.write("Knowledge Base Loaded Successfully!")

chunks = "\n\n".join(documents).split("\n\n")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

st.write("Embeddings Created Successfully!")

st.title("🏢 GMR Real Estate Chatbot")

question = st.text_input(
    "Ask a question about flats, pricing, EMI, GST, etc."
)

if question:

    query_embedding = model.encode([question])

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )

    top_indices = similarities[0].argsort()[-1:][::-1]

    context = ""

    for index in top_indices:
        context += chunks[index] + "\n\n"

    st.subheader("Retrieved Context")

    st.write(context)

    with st.spinner("Generating answer..."):

        answer = generate_answer(
            context,
            question
        )

    st.subheader("Answer")

    st.write(answer) 