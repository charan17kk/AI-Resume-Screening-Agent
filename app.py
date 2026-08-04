from parser import load_all_resumes
from scorer import calculate_similarity
from utils.skills import skill_match_score

with open("jd/job_description.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

resumes = load_all_resumes("resumes")

results = []

for name, text in resumes.items():

    semantic_score = calculate_similarity(job_description, text)

    skill_score, matched, jd_skills = skill_match_score(
        job_description,
        text
    )

    final_score = (
        semantic_score * 0.7 +
        skill_score * 0.3
    )

    results.append({
        "name": name,
        "semantic": semantic_score,
        "skills": skill_score,
        "final": final_score,
        "matched": matched
    })

results = sorted(
    results,
    key=lambda x: x["final"],
    reverse=True
)

print("\n========== FINAL RANKINGS ==========\n")

for i, r in enumerate(results, start=1):

    print(f"{i}. {r['name']}")

    print(f"Semantic : {r['semantic']:.3f}")

    print(f"Skills   : {r['skills']:.3f}")

    print(f"Final    : {r['final']:.3f}")

    print("Matched Skills:")

    print(", ".join(sorted(r["matched"])))

    print("-" * 70)