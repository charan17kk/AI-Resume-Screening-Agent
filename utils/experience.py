import re


def extract_experience(text):
    """
    Extract total years of experience from resume text.
    """

    text = text.lower()

    patterns = [

        r'(\d+)\+?\s*years',

        r'(\d+)\+?\s*year'

    ]

    years = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        years.extend(matches)

    if not years:

        return 0

    return max(int(y) for y in years)


def experience_score(jd_text, resume_text):

    jd_years = extract_experience(jd_text)

    resume_years = extract_experience(resume_text)

    if jd_years == 0:

        return 1.0

    score = min(resume_years / jd_years, 1.0)

    return score