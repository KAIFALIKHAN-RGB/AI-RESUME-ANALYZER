"""
Matches resume skills against skills found in a job description (JD).
"""

from analyzer.skills_list import SKILLS


def jd_match(resume_text, jd_text):
    """
    Compare resume text against skills mentioned in the job description.

    Args:
        resume_text (str): Lowercased resume text.
        jd_text (str): Raw job description text.

    Returns:
        tuple: (matched_skills, missing_skills, match_percentage)
    """
    jd_text = jd_text.lower()

    matched_skills = []
    missing_skills = []

    for skill in SKILLS:
        if skill in jd_text:
            if skill in resume_text:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    total = len(matched_skills) + len(missing_skills)
    match_percentage = (len(matched_skills) / total) * 100 if total > 0 else 0.0

    return matched_skills, missing_skills, match_percentage