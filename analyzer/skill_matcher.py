"""
Analyzes skills found in resume text against a predefined skills list.
"""

from analyzer.skills_list import SKILLS


def analyze_skills(text):
    """
    Compare resume text against the shared SKILLS list.

    Args:
        text (str): Lowercased resume text.

    Returns:
        tuple: (found_skills, missing_skills, all_skills)
    """
    found_skills = []
    missing_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    return found_skills, missing_skills, SKILLS