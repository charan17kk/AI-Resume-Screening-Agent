from parser import load_all_resumes
from scorer import calculate_similarity
from utils.skills import skill_match_score
from utils.experience import experience_score
from utils.education import education_score
from utils.exporter import export_results
from llm import generate_reason

# ----------------------------
# Load Job Description
# ----------------------------
with open("jd/job_description.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

# ----------------------------
# Load Resumes
# ----------------------------
resumes = load_all_resumes("resumes")

results = []

# ----------------------------
# Process Each Resume
# ----------------------------
for name, text in resumes.items():

    # Semantic Similarity
    semantic_score = calculate_similarity(
        job_description,
        text
    )

    # Skill Matching
    skill_score, matched, jd_skills = skill_match_score(
        job_description,
        text
    )

    # Experience Score
    exp_score = experience_score(
        job_description,
        text
    )

    # Education Score
    edu_score = education_score(
        job_description,
        text
    )

    # Final Weighted Score
    final_score = (
        semantic_score * 0.40 +
        skill_score * 0.30 +
        exp_score * 0.20 +
        edu_score * 0.10
    )

    results.append({
        "name": name,
        "semantic": semantic_score,
        "skills": skill_score,
        "experience": exp_score,
        "education": edu_score,
        "final": final_score,
        "matched": matched
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
# Display Results
# ----------------------------
print("\n========== FINAL RANKINGS ==========\n")

for rank, r in enumerate(results, start=1):

    print(f"{rank}. {r['name']}")
    print(f"Semantic Score   : {r['semantic']:.3f}")
    print(f"Skill Score      : {r['skills']:.3f}")
    print(f"Experience Score : {r['experience']:.3f}")
    print(f"Education Score  : {r['education']:.3f}")
    print(f"\nFinal Score      : {r['final']:.3f}")

    print("\nMatched Skills:")
    print(", ".join(sorted(r["matched"])))

    print()

    # ----------------------------
    # AI Recommendation
    # ----------------------------
    try:

        candidate_name = (
            r["name"]
            .replace(".pdf", "")
            .replace("_", " ")
        )

        recommendation = generate_reason(
            candidate_name,
            r["matched"],
            r["final"]
        )

        print("AI Recommendation:")
        print(recommendation)

    except Exception as e:

        print("AI Recommendation:")
        print(f"Could not generate recommendation: {e}")

    print()
    print("-" * 80)

# ----------------------------
# Export CSV & JSON
# ----------------------------
export_results(results)

print("\nFiles saved inside outputs/")