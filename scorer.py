from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Converts text into a semantic embedding vector.
    """
    return model.encode(text)


def calculate_similarity(job_description, resume_text):
    """
    Returns cosine similarity between JD and resume.
    """

    jd_embedding = get_embedding(job_description)

    resume_embedding = get_embedding(resume_text)

    score = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    return float(score)