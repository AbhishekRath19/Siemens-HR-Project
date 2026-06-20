# HR Resume Screener — AI-Powered Candidate Ranking

An AI-driven resume screening system built as part of the Siemens AI Internship Programme. The system uses semantic similarity (not keyword matching) to rank candidates against a job description, and generates AI-written summaries for each candidate using a locally-run LLM.

## What it does

- Accepts a job description and multiple PDF resumes
- Extracts text from resumes using PyPDF2
- Converts text into semantic embeddings using a pre-trained Sentence-Transformer model (`all-MiniLM-L6-v2`)
- Computes a cosine similarity score between the job description and each resume
- Ranks all candidates from highest to lowest match
- Generates a concise AI summary for each candidate using a local LLM (Llama 3.2 via Ollama)
- Displays results in a production-grade React dashboard

## Architecture

This is a two-tier application:

- **`/backend`** — Python FastAPI server exposing a `/analyze` endpoint. Contains all AI logic (embedding model, scoring, PDF extraction, LLM summary generation).
- **`/frontend`** — React + Tailwind + Framer Motion dashboard. Sends job description and resumes to the backend, displays ranked results with metric cards, score bars, and expandable AI summaries.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Tailwind CSS, Framer Motion, Lucide Icons |
| Backend | FastAPI, Uvicorn |
| AI — Scoring | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| AI — Summaries | Ollama running Llama 3.2 (1B, local) |
| PDF Processing | PyPDF2 |
| Data | pandas |

## Running locally

**Backend:**
```bash
cd backend
pip install fastapi uvicorn python-multipart sentence-transformers pypdf2 pandas ollama
uvicorn api:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser. Make sure Ollama is installed and running with the `llama3.2:1b` model pulled.

## Status

Working prototype — built and tested end-to-end. See the accompanying Functional Specification Document for full requirements, architecture, and test case documentation.

---
*Siemens AI Internship Programme — Technology & Innovation*
