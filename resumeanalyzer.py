import streamlit as st
import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_keywords(text):
    # Remove non-alphabet chars, split words, remove short ones
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return list(set(words))

def keyword_match(resume_words, jd_words):
    matched = list(set(resume_words) & set(jd_words))
    missing = list(set(jd_words) - set(resume_words))
    score = round((len(matched) / len(jd_words)) * 100) if jd_words else 0
    return matched, missing, score

st.title("📄 Resume Analyzer + ATS Match")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf", key="resume")
with col2:
    jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf", key="jd")

if resume_file and jd_file:
    with st.spinner("Analyzing..."):
        resume_text = extract_text_from_pdf(resume_file)
        jd_text = extract_text_from_pdf(jd_file)

        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(jd_text)

        matched, missing, score = keyword_match(resume_keywords, jd_keywords)

        st.subheader("✅ ATS Keyword Match Score")
        st.success(f"Match Score: {score}/100")

        st.subheader("🔍 Matched Keywords")
        st.write(", ".join(matched))

        st.subheader("❌ Missing Keywords")
        st.write(", ".join(missing) if missing else "None! Your resume covers all.")
def suggest_better_words(resume_text):
    weak_words = {
        "hardworking": "dedicated",
        "good": "skilled",
        "responsible": "accountable",
        "team player": "collaborative",
        "worked on": "executed",
        "involved in": "led",
        "helped": "supported",
        "made": "developed",
        "handled": "managed",
    }
    suggestions = {}
    for weak, strong in weak_words.items():
        if weak in resume_text.lower():
            suggestions[weak] = strong
    return suggestions

if resume_file and jd_file:
    # (Already existing ATS part here...)

    st.subheader("💡 Word Suggestions for Resume Boost")
    suggestions = suggest_better_words(resume_text)
    if suggestions:
        for weak, strong in suggestions.items():
            st.markdown(f"🔁 Replace **'{weak}'** → **'{strong}'**")
    else:
        st.success("✅ Your resume is using strong words! Good job 🎯")


