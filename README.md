# GMR Real Estate AI Chatbot

An AI-powered real estate assistant built with React, FastAPI, and Groq LLM. Users can ask natural language questions about properties, pricing, home loans, and the buying/renting process and receive intelligent responses in real time.

---

## Live Architecture

```
User
  ↓
React Frontend  (Vite + TailwindCSS)
  ↓  POST /api/chat
FastAPI Backend  (api/index.py)
  ↓
Groq LLM  (llama-3.3-70b-versatile)
  ↓
AI Response back to user
```

---

## Project Structure

```
gmr-rag-chatbot/
├── api/
│   ├── index.py          # FastAPI application — entire backend
│   └── requirements.txt  # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Route definitions
│   │   ├── main.jsx                 # React entry point
│   │   ├── index.css                # Global styles (Tailwind)
│   │   ├── components/              # Reusable UI components
│   │   ├── pages/                   # Page-level components
│   │   ├── layouts/                 # Page layout wrappers
│   │   ├── hooks/                   # Custom React hooks
│   │   ├── services/                # API call logic
│   │   ├── data/                    # Static initial data
│   │   └── utils/                   # Formatter helpers
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── vercel.json           # Vercel deployment configuration
├── .gitignore
└── README.md
```

---

## Component Breakdown

### Backend — `api/index.py`

The entire backend in a single Python file. No database, no FAISS, no local ML models.

**What it does:**
- Receives a user message and conversation history from the frontend
- Prepends a real estate system prompt to every request
- Sends the full conversation to Groq's LLM API
- Returns the AI response

**System Prompt:**
The system prompt instructs the LLM to:
- Only answer real estate related questions
- Help with property search, pricing, home loans, EMI, and documentation
- Politely decline non-real-estate questions
- Recommend licensed agents for final decisions

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Server status + Groq key check |
| POST | `/api/chat` | Send message, receive AI reply |

**Request body for `/api/chat`:**
```json
{
  "message": "What is the average price of a 3 BHK in Bangalore?",
  "history": [
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." }
  ]
}
```

**Response:**
```json
{
  "reply": "The average price of a 3 BHK in Bangalore ranges from...",
  "status": "success"
}
```

---

### Frontend Pages

#### `/` — Landing Page (`LandingPage.jsx`)
Public-facing homepage. Shows the product hero section, feature cards, and a testimonials section. Entry point for new users.

#### `/dashboard` — Dashboard (`DashboardPage.jsx`)
Overview page with key stats (active listings, AI queries, growth metrics) and quick action buttons.

#### `/properties` — Property Search (`PropertySearchPage.jsx`)
Browse and filter property listings. Supports search by city, state, BHK, price range, and bedrooms/bathrooms.

#### `/properties/:id` — Property Detail (`PropertyDetailsPage.jsx`)
Individual property view with image gallery, full description, specs (beds, baths, area), location info, and similar property recommendations.

#### `/chat` — AI Chat Assistant (`ChatAssistantPage.jsx`)
The main AI interface. Users type natural language questions and receive responses from the Groq-powered backend.

---

### Frontend Components

| Component | Purpose |
|-----------|---------|
| `Navbar.jsx` | Top navigation bar with logo and links |
| `TopNavigation.jsx` | Dashboard-level navigation |
| `Sidebar.jsx` | Dashboard sidebar with page links |
| `HeroSection.jsx` | Landing page hero with headline and CTA |
| `PropertyCard.jsx` | Individual property listing card |
| `PropertyGrid.jsx` | Grid layout wrapper for property cards |
| `FilterPanel.jsx` | Filter controls (BHK, price, city, state) |
| `SearchBar.jsx` | Free-text property search input |
| `ChatWindow.jsx` | Chat message display area |
| `ChatInput.jsx` | Message input field and send button |
| `LoadingSkeleton.jsx` | Skeleton loader for async content |
| `Pagination.jsx` | Page navigation for property listings |
| `EmptyState.jsx` | Empty results placeholder |
| `StatCard.jsx` | Dashboard metric cards |
| `FeatureCard.jsx` | Landing page feature highlight cards |
| `SectionHeading.jsx` | Reusable section title with eyebrow text |
| `TestimonialSection.jsx` | Customer testimonial cards |
| `Footer.jsx` | Site footer |

---

### Frontend Layouts

| Layout | Used By |
|--------|---------|
| `PublicLayout.jsx` | Landing page — Navbar + Footer wrapper |
| `DashboardLayout.jsx` | All dashboard pages — Sidebar + TopNavigation |

---

### Frontend Services (`src/services/`)

#### `chatService.js`
Handles all communication with the `/api/chat` endpoint.

```js
chatService.sendMessage(message, history)
// POST /api/chat → { reply, status }
```

#### `propertyService.js`
Handles property listing API calls (`/api/properties`, `/api/properties/:id`, etc.)

---

### Custom Hook — `useChat.js`

Manages the entire chat state in one place:
- `messages` — full conversation array
- `input` — current user input value
- `isTyping` — controls the typing indicator
- `sendMessage()` — calls `chatService`, appends response to messages
- `clearChat()` — resets conversation to initial greeting

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite 7, TailwindCSS 3 |
| Routing | React Router 7 |
| Animation | Framer Motion |
| Icons | Lucide React |
| HTTP client | Axios |
| Backend | FastAPI 0.136, Python 3.12 |
| LLM | Groq — `llama-3.3-70b-versatile` |
| Deployment | Vercel |

---

## About FAISS (Previous Architecture)

This project was originally built with a FAISS-based RAG (Retrieval-Augmented Generation) pipeline. That architecture has been documented here for reference.

### What FAISS Is

FAISS (Facebook AI Similarity Search) is a library for efficient similarity search over dense vectors. It allows searching through millions of high-dimensional vectors (embeddings) in milliseconds.

### How It Was Used in This Project

```
realtor-data.csv  (1.36M US property records)
    ↓
Sentence Transformers (all-MiniLM-L6-v2)
    ↓  encode each property description into a 384-dim vector
numpy array (.npy)
    ↓
FAISS IndexFlatL2
    ↓  build index from all vectors
faiss_index/property_index_full.faiss
    ↓
User query → embed → FAISS search → top-K nearest properties
    ↓
Filter results by metadata (city, state, bed, price)
    ↓
Inject matching properties as context into Groq prompt
    ↓
Groq LLM answers using only those properties as context
```

### Why It Was Removed

| Issue | Detail |
|-------|--------|
| Bundle size | `torch` + `sentence-transformers` + `faiss-cpu` = ~2GB. Vercel's limit is 250MB |
| Cold start | Loading the model + index on first request took 30–90 seconds |
| Complexity | Required a separate build step (`build_full_index.py`) before every deployment |
| Serverless incompatible | FAISS index is a binary file that can't be bundled into a serverless function reliably |

### What Replaced It

The current architecture uses Groq's LLM directly with a detailed system prompt. The LLM uses its own training knowledge to answer real estate questions rather than retrieving from a local dataset.

**Trade-off:** The current version doesn't return specific property listings from a database. It provides general real estate guidance. To restore data-backed property search, a hosted database (e.g. PostgreSQL on Railway, Supabase, or PlanetScale) would replace the local CSV + FAISS setup.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | API key from https://console.groq.com |

Create a `.env` file in the project root:
```
GROQ_API_KEY=gsk_...
```

---

## Running Locally

**Backend:**
```bash
cd gmr-rag-chatbot
venv\Scripts\python.exe -m uvicorn api.index:app --host 127.0.0.1 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

The Vite dev server proxies all `/api` requests to `http://127.0.0.1:8000` automatically.

---

## Deploying to Vercel

1. Push to GitHub
2. Go to https://vercel.com/new
3. Import the repository
4. Add environment variable: `GROQ_API_KEY`
5. Deploy

Vercel reads `vercel.json` automatically — no manual build settings needed.

---

## API Reference

### `GET /api/health`

```json
{
  "status": "ok",
  "groq_configured": true
}
```

### `POST /api/chat`

**Request:**
```json
{
  "message": "How do I calculate EMI for a home loan?",
  "history": []
}
```

**Response:**
```json
{
  "reply": "EMI (Equated Monthly Instalment) is calculated using the formula...",
  "status": "success"
}
```

**Error responses:**

| Code | Reason |
|------|--------|
| 400 | Empty message |
| 503 | GROQ_API_KEY not configured |
| 502 | Groq API unreachable or rate limited |

---

## GitHub Repository

https://github.com/manupulical-44/gmr-rag-chatbot
