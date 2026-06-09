import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

def get_resume_feedback(resume_text, jd_text):

    prompt = f"""
    Analyze the resume against the job description.

    Give:
    1. Resume Strengths
    2. Missing Skills
    3. ATS Optimization Tips
    4. Resume Improvement Suggestions

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    response = model.generate_content(prompt)

    return response.text

if __name__ == "__main__":
    feedback = get_resume_feedback(
        "Python Java SQL HTML CSS",
        "Looking for Python and Machine Learning skills"
    )

    print(feedback)