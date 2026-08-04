import re

# Master list of important skills

SKILLS = [

    # Languages
    "python",
    "sql",
    "java",

    # ML
    "machine learning",
    "deep learning",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "xgboost",

    # NLP
    "nlp",
    "bert",
    "langchain",
    "hugging face",
    "sentence transformers",

    # Data
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",

    # Cloud
    "aws",
    "docker",

    # Tools
    "git",
    "github",
    "streamlit",
    "mysql",
    "postgresql"
]


def extract_skills(text):

    text = text.lower()

    found = set()

    for skill in SKILLS:

        if re.search(r"\b" + re.escape(skill) + r"\b", text):

            found.add(skill)

    return found


def skill_match_score(jd_text, resume_text):

    jd_skills = extract_skills(jd_text)

    resume_skills = extract_skills(resume_text)

    matched = jd_skills.intersection(resume_skills)

    if len(jd_skills) == 0:

        return 0, [], []

    score = len(matched) / len(jd_skills)

    return score, matched, jd_skills