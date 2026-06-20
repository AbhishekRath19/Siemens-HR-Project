from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
import ollama
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def score_resume(job_description, resume_text):
    embeddings = model.encode([job_description, resume_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(score) * 100, 2)

def generate_summary(job_description, resume_text):
    prompt = f"""You are an HR assistant. Read the job description and the candidate resume below.
Write a concise 2-3 sentence summary of this candidate specifically in relation to this job.
Mention their most relevant skills and experience. Be factual and objective.

Job Description:
{job_description}

Resume:
{resume_text}

Summary:"""
    response = ollama.chat(model='llama3.2:1b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

@app.post("/analyze")
async def analyze(job_description: str = Form(...), files: list[UploadFile] = []):
    results = []
    for file in files:
        file_bytes = await file.read()
        resume_text = extract_text_from_pdf(file_bytes)
        score = score_resume(job_description, resume_text)
        summary = generate_summary(job_description, resume_text)
        results.append({
            "candidate": file.filename,
            "score": score,
            "summary": summary
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(results, 1):
        r["rank"] = i
    return {"results": results}