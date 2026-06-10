# GMR Real Estate AI Assistant

This repository now contains the active Python backend for the real-estate AI assistant plus a new React frontend scaffold for the customer-facing experience.

## Backend flow

- `database/prepare_data_v2.py`
- `create_metadata_sample.py`
- `create_embeddings.py`
- `build_faiss.py`
- `app_faiss.py`

## Frontend flow

- `frontend/` contains a React + Vite + Tailwind app with routing, mock services, and production-style UI components.

## Run backend

```bash
streamlit run app_faiss.py
```

## Run API backend

```bash
uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

## Notes

- The old Streamlit RAG entrypoint and scratch utilities were removed.
- API calls in the frontend are isolated in `frontend/src/services/` so the React app can talk to the Python API without UI refactoring.
- The frontend dev server proxies `/api` to the local FastAPI server.
