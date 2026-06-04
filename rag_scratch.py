from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# Load all documents
documents = []

files = [
    "data/flats.txt",
    "data/terms.txt",
    "data/emi.txt"
]

for file_name in files:
    with open(file_name, "r", encoding="utf-8") as file:
        documents.append(file.read())

# Combine documents
text = "\n\n".join(documents)

# Chunking
chunks = text.split("\n\n")

for i, chunk in enumerate(chunks):
    print(f"\n--- CHUNK {i+1} ---")
    print(chunk)

print("Total Chunks:", len(chunks))

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(chunks)

print("Embeddings created successfully!")
def generate_answer(context, question):

    prompt = f"""
You are a helpful assistant for GMR Real Estate.

Answer ONLY using the information provided in the context.

Do not make assumptions.
Do not perform calculations unless explicitly asked.
If information is missing, say that the information is not available.

Only say:
"I could not find that information in the available data."
when the answer is completely absent from the context.

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
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content
# Chat loop
while True:

    query = input("\nAsk a question (or type exit): ")

    # Empty input check
    if query.strip() == "":
        print("Please enter a question.")
        continue

    # Exit
    if query.lower() == "exit":
        print("Goodbye!")
        break

    # Convert query to embedding
    query_embedding = model.encode([query])

    # Calculate similarity
    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )

    # Get top 3 matches
    top_indices = similarities[0].argsort()[-3:][::-1]

    context = ""

    for index in top_indices:
        context += chunks[index] + "\n\n"

    print("\nRETRIEVED CONTEXT:\n")
    print(context)

    answer = generate_answer(
        context,
        query
    )

    print("\nBOT RESPONSE:\n")
    print(answer)