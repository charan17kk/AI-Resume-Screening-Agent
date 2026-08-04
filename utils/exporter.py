import pandas as pd
import json
import os


def export_results(results):

    os.makedirs("outputs", exist_ok=True)

    rows = []

    for rank, r in enumerate(results, start=1):

        rows.append({

            "Rank": rank,
            "Candidate": r["name"],
            "Semantic Score": round(r["semantic"], 3),
            "Skill Score": round(r["skills"], 3),
            "Experience Score": round(r["experience"], 3),
            "Education Score": round(r["education"], 3),
            "Final Score": round(r["final"], 3),
            "Matched Skills": ", ".join(sorted(r["matched"]))
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        "outputs/ranked_candidates.csv",
        index=False
    )

    with open(
        "outputs/ranked_candidates.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rows,
            f,
            indent=4
        )

    print("\nFiles saved inside outputs/")