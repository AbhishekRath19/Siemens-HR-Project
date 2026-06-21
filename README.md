# HR Resume Screener — AI-Powered Candidate Ranking

A fully deployed, end-to-end AI application built as part of the Siemens AI Internship Programme. The system uses semantic similarity (not keyword matching) to rank candidates against a job description, and generates AI-written candidate summaries using a cloud LLM — all wrapped in a production-grade React dashboard.

**Live demo:** [siemens-hr-project.vercel.app](https://siemens-hr-project.vercel.app/)

---

## What it does

- Accepts a job description and multiple PDF resumes
- Extracts text from resumes using PyPDF2
- Converts text into semantic embeddings using a pre-trained Sentence-Transformer model (`all-MiniLM-L6-v2`)
- Computes a cosine similarity score between the job description and each resume — understands *meaning*, not just keywords
- Ranks all candidates from highest to lowest match
- Generates a concise AI summary for each candidate using Groq's hosted LLM (`llama-3.1-8b-instant`)
- Displays results in a polished, dark-themed dashboard with metric cards, skill detection, and expandable AI summaries

## Why semantic matching matters

A job description asking for "machine learning and data science" experience will match a resume that says "artificial intelligence, neural networks, and predictive analytics" — even with **zero shared keywords**. Legacy keyword-based ATS tools would score this 0%. This system recognizes the underlying meaning and scores it correctly. That's the core value of using embeddings instead of string matching.

---

## Live Architecture

This is a real two-tier deployed application — not just code that runs locally.
┌─────────────────────┐         ┌──────────────────────────┐

│   React Dashboard    │  HTTPS  │   FastAPI Backend        │

│   (Vercel)           │ ──────> │   (Hugging Face Spaces)  │

│                      │         │                          │

│  Tailwind, Framer    │ <────── │  Sentence-Transformers   │

│  Motion, Lucide      │  JSON   │  Groq LLM, PyPDF2, pandas│

└─────────────────────┘         └──────────────────────────┘

| Layer | Hosted on | URL |
|---|---|---|
| Frontend | Vercel | [siemens-hr-project.vercel.app](https://siemens-hr-project.vercel.app/) |
| Backend  | Hugging Face Spaces (Docker) | [abhishek-rath19-hr-resume-screener-api.hf.space](https://abhishek-rath19-hr-resume-screener-api.hf.space) |
| Backend API docs | — | [/docs](https://abhishek-rath19-hr-resume-screener-api.hf.space/docs) |

## Repository structure

- **`/backend`** — Python FastAPI server exposing a `/analyze` endpoint. Contains all AI logic: embedding model, scoring, PDF extraction, LLM summary generation. Deployed via Docker to Hugging Face Spaces.
- **`/frontend`** — React + Tailwind + Framer Motion dashboard. Sends job description and resumes to the backend, displays ranked results with metric cards, score bars, and expandable AI summaries. Deployed to Vercel.

## Tech Stack

| Category | Technology |
|---|---|
| Frontend framework | React (Vite) |
| Styling | Tailwind CSS |
| Animation | Framer Motion |
| Icons | Lucide React |
| Frontend hosting | Vercel |
| Backend framework | FastAPI, Uvicorn |
| Backend hosting | Hugging Face Spaces (Docker) |
| Semantic scoring | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| AI summaries | Groq API (`llama-3.1-8b-instant`) |
| PDF processing | PyPDF2 |
| Data handling | pandas |
| Version control | Git / GitHub |

## Why Groq instead of a local LLM?

The original prototype used Ollama running `llama3.2:1b` entirely locally — zero data leaves the machine, zero cost. This works great for local development and is documented as the privacy-first approach in the project's Functional Specification Document.

For cloud deployment, Ollama isn't viable on free hosting tiers: it requires a persistently running process and 2GB+ RAM, while Render and Railway's free tiers cap at 512MB. Groq's free API tier provides the same LLM-summary capability without that infrastructure requirement, making the live demo possible at zero cost. The local-first architecture is preserved in the codebase and can be swapped back in for an on-premise deployment.

## Deployment notes (lessons from getting this live)

A few real infrastructure constraints surfaced while deploying this, worth documenting for anyone extending this project:

- **Render's free tier (512MB RAM) cannot run `sentence-transformers` + `torch`** — the build succeeds but the process crashes on startup with an out-of-memory error. Hugging Face Spaces' free CPU tier (16GB RAM) handles this comfortably.
- **Hugging Face Spaces requires apps to run on port `7860`**, not the conventional `8000`.
- **Environment variables/secrets must be added through the Space's "Variables and secrets" settings**, not as OS-level environment variables — and a Space restart (or Factory Reboot) is sometimes needed for new secrets to be picked up by a running container.
- **CORS origins must match the exact live frontend domain**, not the platform's dashboard URL.

## Running locally

**Backend** (uses Ollama for fully local, zero-cost inference):
```bash
cd backend
pip install -r requirements.txt
ollama pull llama3.2:1b
uvicorn api:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Update the API URL in `src/App.jsx` to `http://localhost:8000/analyze` if testing locally against the Ollama version.

## Documentation

- **Functional Specification Document** — full requirements, architecture, use cases, test cases, and user manual
- **AI Internship Notes (Phases 1–3)** — AI foundations, market research, and enterprise use case analysis
- **Project Presentation (PPTX)** — 12-slide deck covering problem, solution, architecture, live demo, and business impact

## Status

**Working, fully deployed prototype.** Frontend and backend are live and communicating over HTTPS. Tested end-to-end with real resumes and real job descriptions, producing semantically accurate match scores and AI-generated candidate summaries.

### Known limitations (documented, not blockers)

- No persistent storage — results are not saved between sessions (planned: MongoDB integration)
- Scanned/image-based PDFs are not supported (no OCR yet)
- Single-user, no authentication
- Not yet integrated with Siemens HRIS/ATS systems

---

*Siemens AI Internship Programme — Technology & Innovation*