EDUCATION_LEVELS = [

    "phd",

    "master",

    "m.tech",

    "ms",

    "bachelor",

    "b.tech"

]


def education_score(jd_text, resume_text):

    jd = jd_text.lower()

    resume = resume_text.lower()

    for degree in EDUCATION_LEVELS:

        if degree in jd:

            if degree in resume:

                return 1.0

            else:

                return 0.0

    return 1.0