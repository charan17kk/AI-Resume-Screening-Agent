import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_reason(candidate_name, matched_skills, final_score):

    if final_score >= 0.75:
        recommendation = "Strongly Recommend for Interview"
    elif final_score >= 0.50:
        recommendation = "Consider for Interview"
    else:
        recommendation = "Not Recommended"

    prompt = f"""
You are an experienced Technical Recruiter.

Candidate Name:
{candidate_name}

Final Score:
{final_score:.2f}

Recommendation:
{recommendation}

Matched Skills:
{', '.join(sorted(matched_skills))}

Instructions:

1. If the recommendation is "Strongly Recommend for Interview":
   - Highlight the candidate's strongest technical skills.
   - Explain why they are an excellent match.
   - End with "Recommendation: Strongly Recommend for Interview."

2. If the recommendation is "Consider for Interview":
   - Mention both strengths and areas for improvement.
   - Explain what skills are missing or weaker.
   - End with "Recommendation: Consider for Interview."

3. If the recommendation is "Not Recommended":
   - Politely explain why the profile is not a strong match.
   - Mention important missing skills.
   - End with "Recommendation: Not Recommended."

Keep the response under 100 words.
Use 3-5 bullet points.
Be professional and realistic.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content