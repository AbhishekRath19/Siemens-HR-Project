from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
from groq import Groq
import os
import io
import pdfplumber
from docx import Document
import json

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://siemens-hr-project.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)
allow_origins=[
    "http://localhost:5173",
    "https://siemens-hr-project.vercel.app",
    "https://siemens-legal-project-b0ofsoe0p-abhishekrath19s-projects.vercel.app"
],

model = SentenceTransformer('all-MiniLM-L6-v2')

# ── Legal Contract Screener — Risk Library ────────────────────────────────────

RISK_LIBRARY = {
    "auto_renewal": {
        "severity": "High",
        "examples": [
            "This Agreement shall automatically renew for successive one-year terms unless either party provides written notice of termination at least 90 days prior to expiration.",
            "The term shall renew automatically unless cancelled in writing 60 days before the end of the current term.",
            "This Agreement will continue in full force and effect and will automatically renew unless terminated by written notice.",
            "Absent written notice of termination provided no less than 30 days prior to the end of any term, this Agreement shall automatically renew.",
            "The Agreement automatically extends for additional periods equal to the initial term unless a party elects not to renew by providing advance written notice.",
        ]
    },
    "unilateral_termination": {
        "severity": "High",
        "examples": [
            "Company may terminate this Agreement at any time, with or without cause, in its sole discretion upon written notice.",
            "Either party may terminate this Agreement at will with 30 days written notice, however Company reserves the right to terminate immediately.",
            "The Disclosing Party may terminate this Agreement at any time without liability or obligation.",
            "Company shall have the right to terminate this Agreement immediately and without prior notice at its sole discretion.",
            "The Agreement may be terminated by the Company for any reason or for no reason upon notice to the other party.",
        ]
    },
    "uncapped_liability": {
        "severity": "High",
        "examples": [
            "The Receiving Party shall be liable for any and all damages arising from unauthorized disclosure of Confidential Information.",
            "In the event of a breach, the breaching party shall be responsible for all losses, damages, and expenses of any kind.",
            "Receiving Party agrees to indemnify Disclosing Party for all direct, indirect, incidental, and consequential damages.",
            "The party in breach shall bear unlimited financial responsibility for all resulting damages without limitation.",
            "There shall be no limitation on the liability of the Receiving Party for breach of this Agreement.",
        ]
    },
    "one_sided_indemnification": {
        "severity": "Medium",
        "examples": [
            "Receiving Party shall indemnify, defend, and hold harmless Disclosing Party from any and all claims arising from Receiving Party's breach.",
            "The Receiving Party agrees to indemnify and hold harmless the Disclosing Party from any losses, costs, or damages.",
            "Receiving Party shall bear all costs of defense and indemnify Disclosing Party against any third-party claims.",
            "The indemnifying party shall assume full responsibility for all claims, damages, losses, and expenses including attorney fees.",
            "Receiving Party will indemnify Disclosing Party for any and all claims, demands, losses, or liabilities of any nature.",
        ]
    },
    "unfavorable_jurisdiction": {
        "severity": "Medium",
        "examples": [
            "This Agreement shall be governed by the laws of the State of Delaware and any disputes shall be resolved exclusively in Delaware courts.",
            "The parties agree that exclusive jurisdiction for any dispute shall lie with the courts of England and Wales.",
            "Any legal proceedings arising from this Agreement must be brought exclusively in the courts of Singapore.",
            "This Agreement is governed by the laws of New York and the parties consent to exclusive jurisdiction in New York County.",
            "All disputes shall be subject to binding arbitration in a location designated solely by the Disclosing Party.",
        ]
    },
    "vague_confidentiality_scope": {
        "severity": "Low",
        "examples": [
            "Confidential Information includes any and all information disclosed by either party, including but not limited to business plans, financial data, and technical information.",
            "All information shared between the parties shall be considered Confidential Information regardless of whether it is marked as such.",
            "Confidential Information means any information of any nature and in any form disclosed by Disclosing Party.",
            "The term Confidential Information shall be broadly construed to include all information disclosed in any manner.",
            "Any information disclosed by either party, whether written or verbal, shall be deemed Confidential Information.",
        ]
    },
}

RISK_EMBEDDINGS = {}
KEYWORD_PATTERNS = {
    "auto_renewal":              ["automatically renew", "auto-renew", "unless cancelled", "unless terminated in writing"],
    "unilateral_termination":    ["at any time", "sole discretion", "without cause", "without liability"],
    "uncapped_liability":        ["any and all damages", "without limitation", "unlimited liability", "all losses"],
    "one_sided_indemnification": ["indemnify and hold harmless", "indemnify, defend", "bear all costs"],
    "unfavorable_jurisdiction":  ["exclusive jurisdiction", "exclusively in the courts", "binding arbitration"],
    "vague_confidentiality_scope": ["any and all information", "regardless of whether", "broadly construed"],
}
SIMILARITY_THRESHOLD = 0.45

def precompute_risk_embeddings():
    for category, data in RISK_LIBRARY.items():
        RISK_EMBEDDINGS[category] = model.encode(data["examples"], convert_to_tensor=True)

precompute_risk_embeddings()

def legal_extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass
    if not text.strip():
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def legal_extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


def segment_into_clauses(text: str) -> list:
    import re
    pattern = re.compile(
        r'(?m)^('
        r'\d+(?:\.\d+)*\.?\s+[A-Z]'
        r'|Section\s+\d+'
        r'|SECTION\s+\d+'
        r'|Article\s+\d+'
        r'|ARTICLE\s+[IVX]+'
        r'|[A-Z][A-Z\s]{4,}(?=\n)'
        r')'
    )
    clauses = []
    matches = list(pattern.finditer(text))
    if matches:
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            clause_text = text[start:end].strip()
            if len(clause_text) < 20:
                continue
            lines = clause_text.split("\n", 1)
            heading = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else clause_text
            clauses.append({"index": i, "heading": heading, "text": body, "full_text": clause_text})
    else:
        import re as re2
        paragraphs = [p.strip() for p in re2.split(r'\n\s*\n', text) if len(p.strip()) > 40]
        for i, para in enumerate(paragraphs):
            clauses.append({"index": i, "heading": f"Paragraph {i+1}", "text": para, "full_text": para})
    return clauses


def check_clause_for_risk(clause_text: str) -> list:
    triggered = []
    clause_embedding = model.encode(clause_text, convert_to_tensor=True)
    for category, risk_embeddings in RISK_EMBEDDINGS.items():
        scores = util.cos_sim(clause_embedding, risk_embeddings)
        max_score = float(scores.max())
        keyword_hit = any(kw.lower() in clause_text.lower() for kw in KEYWORD_PATTERNS.get(category, []))
        if max_score >= SIMILARITY_THRESHOLD or keyword_hit:
            triggered.append({
                "category": category,
                "similarity_score": round(max_score * 100, 1),
                "keyword_hit": keyword_hit,
                "severity": RISK_LIBRARY[category]["severity"]
            })
    return triggered


def get_llm_risk_assessment(clause_text: str, triggered_categories: list) -> dict:
    categories_str = ", ".join([t["category"].replace("_", " ") for t in triggered_categories])
    prompt = f"""You are an expert legal analyst reviewing a contract clause for risk.
The following clause has been flagged as potentially risky in these categories: {categories_str}

Clause text:
\"\"\"{clause_text}\"\"\"

Provide your analysis in this exact JSON format (no other text):
{{
  "severity": "High" or "Medium" or "Low",
  "risk_category": "the single most relevant risk category from: auto_renewal, unilateral_termination, uncapped_liability, one_sided_indemnification, unfavorable_jurisdiction, vague_confidentiality_scope",
  "explanation": "2-3 sentences explaining why this clause is risky in plain English",
  "suggestion": "A specific actionable suggested rewording or fix for this clause"
}}"""
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "severity": triggered_categories[0]["severity"] if triggered_categories else "Medium",
            "risk_category": triggered_categories[0]["category"] if triggered_categories else "unknown",
            "explanation": raw,
            "suggestion": "Please review this clause with legal counsel."
        }

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
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
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

@app.post("/legal/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    file_bytes = await file.read()

    if file.filename.lower().endswith(".pdf"):
        raw_text = legal_extract_text_from_pdf(file_bytes)
    elif file.filename.lower().endswith(".docx"):
        raw_text = legal_extract_text_from_docx(file_bytes)
    else:
        return {"error": f"Unsupported file type: {file.filename}"}

    if not raw_text.strip():
        return {"error": "Could not extract text. File may be image-based."}

    clauses = segment_into_clauses(raw_text)
    flagged_clauses = []
    clean_clauses = []

    for clause in clauses:
        if len(clause["full_text"].split()) < 15:
            clean_clauses.append(clause)
            continue
        triggered = check_clause_for_risk(clause["full_text"])
        if triggered:
            assessment = get_llm_risk_assessment(clause["full_text"], triggered)
            flagged_clauses.append({
                "index": clause["index"],
                "heading": clause["heading"],
                "text": clause["text"],
                "full_text": clause["full_text"],
                "triggered_categories": triggered,
                "severity": assessment.get("severity", "Medium"),
                "risk_category": assessment.get("risk_category", "unknown"),
                "explanation": assessment.get("explanation", ""),
                "suggestion": assessment.get("suggestion", ""),
            })
        else:
            clean_clauses.append(clause)

    severity_order = {"High": 0, "Medium": 1, "Low": 2}
    flagged_clauses.sort(key=lambda x: severity_order.get(x["severity"], 3))

    return {
        "filename": file.filename,
        "total_clauses": len(clauses),
        "flagged_count": len(flagged_clauses),
        "clean_count": len(clean_clauses),
        "risk_summary": {
            "high": sum(1 for f in flagged_clauses if f["severity"] == "High"),
            "medium": sum(1 for f in flagged_clauses if f["severity"] == "Medium"),
            "low": sum(1 for f in flagged_clauses if f["severity"] == "Low"),
        },
        "flagged_clauses": flagged_clauses,
    }