"""
Calculates a resume score based on matched skills.
"""


def calculate_score(found_skills, total_skills):
    """
    Calculate the resume score as a percentage.

    Args:
        found_skills (list): Skills found in the resume.
        total_skills (int): Total number of skills checked.

    Returns:
        float: Score between 0.0 and 100.0.
    """
    found_count = len(found_skills)
    score = (found_count / total_skills) * 100 if total_skills > 0 else 0.0
    return score