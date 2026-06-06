def jd_match(resume_text, jd_text):

    jd_text = jd_text.lower()

    skills = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "machine learning",
        "data analysis"
    ]

    matched_skills = []
    missing_skills = []

    for skill in skills:

        if skill in jd_text:

            if skill in resume_text:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    if len(matched_skills) + len(missing_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = (
            len(matched_skills)
            / (len(matched_skills) + len(missing_skills))
        ) * 100

    return matched_skills, missing_skills, match_percentage