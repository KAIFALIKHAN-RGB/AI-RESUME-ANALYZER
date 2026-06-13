import json

response = """
{
    "profession": "Software Developer",
    "resume_skills": ["Java", "Spring Boot", "SQL"],
    "matched_skills": ["Java", "Spring Boot"],
    "missing_skills": ["SQL"],
    "match_percentage": 85,
    "feedback": "Your resume matches 85% of the required skills for the Software Developer position. Consider adding SQL to improve your match percentage."
}
"""

data = json.loads(response)

print(data["profession"])
print(data["resume_skills"])
print(data["match_percentage"])

for skill in data["resume_skills"]:
    print(skill)

import streamlit as st

st.title("JSON Test")

st.subheader("Profession")
st.write(data["profession"])

st.subheader("Skills")
for skill in data["resume_skills"]:
    st.write("✅ " + skill)

st.subheader("Match Percentage")
st.write(f"{data['match_percentage']}%")
st.subheader("Matched Skills")

for skill in data["matched_skills"]:
    st.write("✅ " + skill)

st.subheader("Missing Skills")

for skill in data["missing_skills"]:
    st.write("❌ " + skill)

st.subheader("Feedback")
st.write(data["feedback"])
