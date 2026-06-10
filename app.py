from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="GMR Real Estate Chatbot",
    page_icon="🏢",
    layout="centered" 
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_data
def load_documents():

    documents = []

    files = [
        "data/flats.txt",
        "data/terms.txt",
        "data/emi.txt"
    ]

    for file_name in files:

        with open(file_name, "r", encoding="utf-8") as file:
            documents.append(file.read())

    return documents

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_data
def create_embeddings(chunks):

    model = load_model()

    return model.encode(chunks)

def generate_answer(context, question, chat_history):

    prompt = f"""
You are a professional GMR Real Estate Sales Executive.

Your job is to help customers with:

- Flat availability
- Pricing
- Booking
- EMI
- Documentation
- GST
- Registration
- Property policies

Rules:

1. Use ONLY the information provided in the Context.
2. Never make up information.
3. Never answer unrelated topics.
4. Be friendly and professional.
5. Speak like a real estate executive.
6. Use Conversation History when needed.
7. Do not perform calculations unless explicitly requested.
8. If information is unavailable, say:

"I don't have that information in the current project details."

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
        max_tokens=300
    )

    return response.choices[0].message.content

st.title("🏢 GMR Real Estate Chatbot")

st.caption(
    "Ask about flats, pricing, booking, EMI, GST, documents, and more."
)

documents = load_documents()

chunks = "\n\n".join(documents).split("\n\n")

model = load_model()

embeddings = create_embeddings(chunks)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input(
    "Ask about GMR Real Estate..."
)

if question:

    # Show User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    if question.lower().strip() in greetings:

        answer = (
            "Hello! Welcome to GMR Real Estate. "
            "How can I assist you today? "
            "We currently offer 2 BHK, 3 BHK, and 4 BHK apartments."
        )

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.stop()

    real_estate_keywords = [
        "flat",
        "flats",
        "apartment",
        "apartments",
        "bhk",
        "price",
        "pricing",
        "cost",
        "booking",
        "emi",
        "loan",
        "gst",
        "document",
        "documents",
        "property",
        "properties",
        "registration",
        "cancel",
        "cancellation",
        "possession",
        "down payment",
        "availability",
        "available"
    ]

    followup_keywords = [
        "its",
        "it",
        "that",
        "this",
        "them",
        "those",
        "these",
        "how many",
        "what about"
    ]

    is_real_estate_query = any(
        keyword in question.lower()
        for keyword in real_estate_keywords
    )

    is_followup_query = any(
        keyword in question.lower()
        for keyword in followup_keywords
    )

    if not is_real_estate_query and not is_followup_query:

        answer = (
            "I can assist only with GMR Real Estate related queries such as:\n\n"
            "• Flat availability\n"
            "• Pricing\n"
            "• Booking process\n"
            "• EMI options\n"
            "• GST\n"
            "• Required documents\n"
            "• Registration details"
        )

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.stop()

    query_embedding = model.encode([question])

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )

    max_similarity = similarities.max()

    if max_similarity < 0.25:

        answer = (
            "I could not find relevant information in the GMR Real Estate knowledge base."
        )

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.stop()

    top_indices = similarities[0].argsort()[-3:][::-1]

    context = ""

    for index in top_indices:
        context += chunks[index] + "\n\n"

    history = []

    for msg in st.session_state.messages[-10:]:

        history.append(
            f"{msg['role']}: {msg['content']}"
        )

    chat_history = "\n".join(history)

    with st.spinner("Generating answer..."):

        answer = generate_answer(
            context=context,
            question=question,
            chat_history=chat_history
        )

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )