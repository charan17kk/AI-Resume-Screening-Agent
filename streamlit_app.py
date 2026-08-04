import os
import streamlit as st
import pandas as pd

from parser import load_all_resumes
from scorer import calculate_similarity
from utils.skills import skill_match_score
from utils.experience import experience_score
from utils.education import education_score
import shutil
from llm import generate_reason

candidate_names = {
    "Charan_Resume.pdf": "Kandukuri Sai Charan",
    "Aarav_ML_Engineer.pdf": "Aarav Sharma",
    "Priya_Data_Scientist.pdf": "Priya Nair",
    "Rahul_Python_Developer.pdf": "Rahul Verma",
    "Neha_Data_Analyst.pdf": "Neha Patel",
    "Rohan_Frontend_Developer.pdf": "Rohan Gupta"
}

st.set_page_config(
    page_title="AI-Powered Resume Screening System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered Resume Screening System")

st.write(
    """
Paste a Job Description and upload candidate resumes.

The AI automatically evaluates semantic similarity, technical skills,
experience, education, and generates hiring recommendations.
"""
)
st.divider()

job_description = st.text_area(
    "📄 Paste Job Description",
    height=320,
    placeholder="""
Paste the complete Job Description here...

Example:

Job Title: Machine Learning Engineer

Responsibilities:
- Build ML models
- Develop NLP applications
- Work with Python

Skills:
Python
SQL
Machine Learning
Scikit-learn
Pandas
Numpy
"""
)

resume_files = st.file_uploader(
    "📂 Upload Candidate Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button("🚀 Start AI Screening", use_container_width=True):

    if not job_description.strip():
        st.error("Please paste a Job Description.")
        st.stop()

    if not resume_files:
        st.error("Please upload one or more resumes.")
        st.stop()

    # ----------------------------
    # Prepare Resume Folder
    # ----------------------------
    if os.path.exists("resumes"):
        shutil.rmtree("resumes")

    os.makedirs("resumes")

    # Save uploaded resumes
    for file in resume_files:
        with open(f"resumes/{file.name}", "wb") as f:
            f.write(file.getbuffer())

    # ----------------------------
    # AI Analysis
    # ----------------------------
    with st.spinner("🤖 AI is analyzing candidates..."):

        resumes = load_all_resumes("resumes")

        results = []

        for name, text in resumes.items():

            semantic_score = calculate_similarity(
                job_description,
                text
            )

            skill_score, matched, jd_skills = skill_match_score(
                job_description,
                text
            )

            exp_score = experience_score(
                job_description,
                text
            )

            edu_score = education_score(
                job_description,
                text
            )

            final_score = (
                semantic_score * 0.40 +
                skill_score * 0.30 +
                exp_score * 0.20 +
                edu_score * 0.10
            )

            if final_score >= 0.75:
                decision = "🟢 Interview"
            elif final_score >= 0.50:
                decision = "🟡 Consider"
            else:
                decision = "🔴 Reject"

            results.append({
                "name": name,
                "semantic": round(semantic_score, 3),
                "skills": round(skill_score, 3),
                "experience": round(exp_score, 3),
                "education": round(edu_score, 3),
                "final": round(final_score, 3),
                "decision": decision,
                "matched": ", ".join(sorted(matched))
            })

    # ----------------------------
    # Sort Results
    # ----------------------------
    results = sorted(
        results,
        key=lambda x: x["final"],
        reverse=True
    )

    # ----------------------------
    # Ranking Table
    # ----------------------------
    st.subheader("🏆 Candidate Rankings")

    df = pd.DataFrame(results)

    display_df = df[
        [
            "name",
            "final",
            "decision",
            "semantic",
            "skills",
            "experience",
            "education"
        ]
    ].copy()

    display_df.columns = [
        "Candidate",
        "Final Score",
        "Decision",
        "Semantic",
        "Skills",
        "Experience",
        "Education"
    ]

    # Show actual names
    display_df["Candidate"] = display_df["Candidate"].map(
        lambda x: candidate_names.get(x, x)
    )

    # Convert final score to %
    display_df["Final Score"] = (
        display_df["Final Score"] * 100
    ).round(1).astype(str) + "%"

    display_df.index = range(1, len(display_df) + 1)

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # ----------------------------
    # Best Candidate
    # ----------------------------
    best = results[0]

    st.divider()

    st.subheader("🥇 Best Candidate")

    best_name = candidate_names.get(best["name"], best["name"])

    st.success(
        f"""
**{best_name}**

✅ Final Score: **{best['final']*100:.1f}%**

Decision: **{best['decision']}**
"""
    )

    # ----------------------------
    # AI Recommendations
    # ----------------------------
    st.divider()

    st.subheader("🤖 AI Recommendations")

    for r in results:

        candidate_name = candidate_names.get(
            r["name"],
            r["name"].replace(".pdf", "").replace("_", " ")
        )

        with st.expander(candidate_name):

            recommendation = generate_reason(
                candidate_name,
                r["matched"].split(", "),
                r["final"]
            )

            st.write(recommendation)

    # ----------------------------
    # Download CSV
    # ----------------------------
    st.divider()

    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Rankings (CSV)",
        csv,
        "candidate_rankings.csv",
        "text/csv",
        use_container_width=True
    )