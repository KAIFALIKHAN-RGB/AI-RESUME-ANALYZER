def analyze_skills(text):

    skills = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "machine learning",
        "data analysis"
    ]

    found_skills = []
    missing_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    return found_skills, missing_skills, skills