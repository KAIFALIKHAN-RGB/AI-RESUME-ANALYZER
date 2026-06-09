import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

def get_resume_feedback(resume_text, jd_text):

    prompt = f"""
    Analyze the resume against the job description.

    Give ONLY the following feedback in a concise format:
    1. Top 3 Resume Strengths
    2. Top 3 Missing Skills
    3. Top 3 ATS Optimization Tips
    4. Top 3 Resume Improvement Suggestions

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