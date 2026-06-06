def calculate_score(found_skills, total_skills):

    found_count = len(found_skills)

    score = (found_count / total_skills) * 100

    return score