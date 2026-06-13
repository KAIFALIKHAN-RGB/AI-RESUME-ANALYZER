import google.generativeai as genai
import json
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_jd(jd_text):

    prompt = f"""
    Analyze this job description.

    Return ONLY valid JSON.

    {{
        "skills": []
    }}

    Job Description:
    {jd_text}
    """

    response = model.generate_content(prompt)

    cleaned = response.text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    return json.loads(cleaned)