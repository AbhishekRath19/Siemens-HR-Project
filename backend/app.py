import streamlit as st
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
import pandas as pd
import ollama

st.set_page_config(page_title="HR Resume Screener", page_icon="📄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 20% 0%, #16213E 0%, #0B0E14 45%, #0B0E14 100%);
}

/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #131722 0%, #0E1117 100%);
    border-right: 1px solid #232838;
}
[data-testid="stSidebar"] h2 {
    color: #E8EAED;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 0.3px;
    border-left: 3px solid #4F8DFD;
    padding-left: 10px;
    margin-bottom: 4px;
}

/* Hero header card */
.hero-card {
    background: linear-gradient(135deg, #1B2740 0%, #131A2B 100%);
    border: 1px solid #29314A;
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
.hero-badge {
    display: inline-block;
    background: rgba(79,141,253,0.15);
    color: #4F8DFD;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    border: 1px solid rgba(79,141,253,0.3);
}
.hero-title {
    color: #F5F6FA;
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: #9AA4B8;
    font-size: 1.02rem;
    margin: 0;
    line-height: 1.5;
}

/* Text area */
.stTextArea textarea {
    background-color: #131722 !important;
    border: 1px solid #29314A !important;
    border-radius: 10px !important;
    color: #E8EAED !important;
}
.stTextArea textarea:focus {
    border-color: #4F8DFD !important;
    box-shadow: 0 0 0 1px #4F8DFD !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
    background-color: #131722;
    border: 1.5px dashed #29314A;
    border-radius: 12px;
}
[data-testid="stFileUploader"]:hover section {
    border-color: #4F8DFD;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg, #4F8DFD 0%, #3D6FD9 100%);
    color: white;
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 10px;
    border: none;
    padding: 0.7rem 1rem;
    width: 100%;
    box-shadow: 0 4px 14px rgba(79,141,253,0.35);
    transition: all 0.2s ease;
}
.stButton button:hover {
    background: linear-gradient(135deg, #5C98FF 0%, #4878E0 100%);
    box-shadow: 0 6px 20px rgba(79,141,253,0.5);
    transform: translateY(-1px);
}

/* Subheaders */
h3 {
    color: #E8EAED !important;
    font-weight: 700 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #29314A;
    border-radius: 12px;
    overflow: hidden;
}

/* Metric-style score cards (used later) */
.score-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

model = SentenceTransformer('all-MiniLM-L6-v2')
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def score_resume(job_description, resume_text):
    embeddings = model.encode([job_description, resume_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(score) * 100, 2)
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file):
    reader = PdfReader(file)
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

    response = ollama.chat(
        model='llama3.2:1b',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']
st.markdown("""
<div class="hero-card">
    <div class="hero-badge">SIEMENS · AI INTERNSHIP PROJECT</div>
    <p class="hero-title">🤖 HR Resume Screener</p>
    <p class="hero-sub">Upload candidate resumes and a job description — AI instantly ranks every candidate by semantic match score, no keyword guesswork required.</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.header("Job Description")
job_description = st.sidebar.text_area("Paste the job description here", height=300)

st.sidebar.header("Upload Resumes")
uploaded_files = st.sidebar.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)

analyse_button = st.sidebar.button("Analyse Candidates")

if analyse_button:
    if not job_description:
        st.warning("Please paste a job description in the sidebar.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        st.subheader("📊 Candidate Rankings")
        results = []

        for file in uploaded_files:
            resume_text = extract_text_from_pdf(file)
            score = score_resume(job_description, resume_text)
            with st.spinner(f"Generating summary for {file.name}..."):
                summary = generate_summary(job_description, resume_text)
            results.append({"Candidate": file.name, "Match Score (%)": score, "AI Summary": summary})

        df = pd.DataFrame(results)
        df = df.sort_values("Match Score (%)", ascending=False)
        df.insert(0, "Rank", range(1, len(df) + 1))
        df = df.reset_index(drop=True)

        st.dataframe(
            df[["Rank", "Candidate", "Match Score (%)"]],
            use_container_width=True
        )

        st.subheader("📝 Candidate Summaries")
        for _, row in df.iterrows():
            with st.expander(f"#{row['Rank']} — {row['Candidate']} ({row['Match Score (%)']}%)"):
                st.write(row["AI Summary"])

        st.subheader("📈 Score Distribution")
        st.bar_chart(df.set_index("Candidate")["Match Score (%)"])