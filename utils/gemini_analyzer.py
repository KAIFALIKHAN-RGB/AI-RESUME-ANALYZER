import os
import streamlit as st
import google.generativeai as genai
import json

# Configure API key from environment or Streamlit secrets
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(resume_text,jd_text=None):
    if jd_text and jd_text.strip():
        prompt = f"""
        Analyze the following resume against the job description.
        Identify the candidate's profession.

        Extract maximum 10 important resume skills.

        Extract maximum 10 important JD skills.

        Find matched skills between resume and JD.

        Find missing JD skills.

        Calculate realistic match percentage.

        Generate 3-5 strengths.

        Generate 3-5 weaknesses.

        Generate actionable feedback for improving the resume.

        Return ONLY one valid JSON object.
        {{
         "profession": "",
         "resume_skills": [],
         "jd_skills": [],
         "matched_skills": [],
         "missing_skills": [],
         "match_percentage": 0,
         "strengths": [],
         "weaknesses": [],
         "resume_score": 0.0,
         "feedback": ""
        }}
        Resume:
        {resume_text}
        Job Description:
        {jd_text}
        """
    else:

      prompt = f"""
      Analyze the following resume only. Since no job description is provided, focus on identifying the profession, key skills, strengths, and weaknesses based on the resume content.
      Identify the candidate's profession.

      Extract the 10 most important skills found in the resume.

      Generate 5 profession-specific important skills that are commonly required for the detected profession but are missing from the resume.

      Store these missing skills in "missing_resume_skills".

      Do not generate generic skills. Generate only skills relevant to the detected profession.
      Return ONLY one valid JSON object.

      {{
       "profession": "",
       "resume_skills": [],
       "missing_resume_skills": [],
       "jd_skills": [],
       "matched_skills": [],
       "missing_skills": [],
       "match_percentage": 0,
       "strengths": [],
       "weaknesses": [],
       "resume_score": 0.0,
      "feedback": ""
     }}
     Generate resume_score between 0 and 100.

        Consider:
        - Skills
        - Projects
        - Experience
        - Education
        - Resume completeness

        Provide actionable feedback.

    Resume:
    {resume_text}
    Job Description:
    {jd_text}
    """
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise RuntimeError("Gemini API request failed. Please check your API key and network connection.") from e

    cleaned_response = response.text.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.replace("```json", "")
        cleaned_response = cleaned_response.replace("```", "")
        cleaned_response = cleaned_response.strip()
    
    try:
        return json.loads(cleaned_response)
    except Exception:
        return {
            "profession": "Unknown",
            "resume_skills": [],
            "missing_resume_skills": [],
            "jd_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0,
            "strengths": [],
            "weaknesses": [],
            "resume_score": 0.0,
            "feedback": "Unable to generate feedback"

        }
        