# 🏢 GMR Real Estate RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using Python, Sentence Transformers, Groq LLM, and Streamlit.

## 📌 Project Overview

This chatbot answers questions related to:

* Flat availability
* Flat pricing
* Booking amount
* GST information
* EMI details
* Loan tenure options
* Required documents
* Cancellation policies

The chatbot retrieves relevant information from a custom knowledge base and uses a Groq LLM to generate accurate responses based on the retrieved context.

---

##  Technologies Used

* Python
* Streamlit
* Sentence Transformers
* Scikit-Learn
* Groq API
* Python Dotenv

---

## Project Structure

```text
gmr-rag-chatbot/
│
├── data/
│   ├── flats.txt
│   ├── terms.txt
│   └── emi.txt
│
├── .env
├── app.py
├── rag_scratch.py
├── requirements.txt
└── README.md
```

---

## RAG Workflow

1. Load knowledge base documents.
2. Split documents into chunks.
3. Generate embeddings using SentenceTransformer.
4. Convert user query into an embedding.
5. Calculate cosine similarity.
6. Retrieve the most relevant context.
7. Send context and question to Groq LLM.
8. Generate and display the final answer.

---

## Knowledge Base

### Flats Information

* 2 BHK: 30 Units

  * Base Price: ₹1 Crore
  * Negotiation Start Price: ₹1.2 Crore
  * Minimum Negotiation Price: ₹90 Lakhs

* 3 BHK: 50 Units

  * Base Price: ₹1.5 Crore
  * Negotiation Start Price: ₹1.7 Crore
  * Minimum Negotiation Price: ₹1.3 Crore

* 4 BHK: 20 Units

  * Base Price: ₹2 Crore
  * Negotiation Start Price: ₹2.2 Crore
  * Minimum Negotiation Price: ₹1.8 Crore

### Terms & Conditions

* Booking Amount: 10% of property value
* Required Documents:

  * Aadhaar Card
  * PAN Card
  * Address Proof
* GST Applicable
* Registration Charges Separate
* Flat Allotment Subject to Availability
* Cancellation Before Agreement: 5% Deduction
* Cancellation After Agreement: 10% Deduction

### EMI Information

* Minimum Down Payment: 20%
* Loan Tenure Options:

  * 5 Years
  * 10 Years
  * 15 Years
  * 20 Years
  * 25 Years
  * 30 Years
* Interest Rate Depends on Partner Banks
* EMI Depends on Loan Amount, Tenure, Interest Rate, and Bank Approval

---

## Installation

Clone the repository:

```bash
git clone https://github.com/manupulical-44/gmr-rag-chatbot.git
```

Move into the project directory:

```bash
cd gmr-rag-chatbot
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶Run the Application

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

---

## Sample Questions

* What is the booking amount?
* What documents are required?
* Is GST applicable?
* What is the minimum price of a 4 BHK?
* What loan tenures are available?
* What happens if I cancel after agreement?

---

## 👨Author

Manu Pulical

Built as a learning project to understand Retrieval-Augmented Generation (RAG), embeddings, semantic search, Groq LLM integration, and Streamlit application development.

## Demo Capabilities

The chatbot can:

- Answer questions about 2 BHK, 3 BHK, and 4 BHK apartments
- Provide pricing and availability information
- Explain booking amount and required documents
- Provide EMI and loan tenure information
- Explain cancellation policies
- Maintain conversation context for follow-up questions
- Politely reject unrelated queries
- Interact in a conversational real-estate executive style


## Features

- Retrieval Augmented Generation (RAG)
- Sentence Transformer Embeddings
- Cosine Similarity Search
- Groq LLM Integration
- Streamlit Chat Interface
- Conversation Memory
- Greeting Detection
- Irrelevant Query Filtering
- Similarity Threshold Validation
- Real Estate Executive Style Responses
- Context-Aware Follow-up Questions


## Enhancements Based on Manager Feedback

The chatbot was enhanced to provide a more natural and user-friendly conversational experience.

### Improvements Added

- Added greeting support (Hi, Hello, Good Morning, etc.)
- Added conversational real-estate executive style responses
- Added conversation memory for follow-up questions
- Added irrelevant query detection and rejection
- Added similarity threshold validation
- Added ChatGPT-style Streamlit chat interface
- Improved prompt engineering for grounded responses
- Improved overall user experience and interaction flow

## chnages made
