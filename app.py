import streamlit as st
from resume.pdf_reader import extract_pdf_text
from resume.docx_reader import extract_docx_text

from analyzer.skill_matcher import analyze_skills
from analyzer.scorer import calculate_score
from analyzer.jd_matcher import jd_match


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

with st.sidebar:

    st.header("About")

    st.write(
        """
        Upload your resume and compare it
        against a job description.
        """
    )

st.markdown("""
<div style='text-align:center'>
<h1>📄 AI Resume Analyzer</h1>
<h4>Get Resume Score, Skill Analysis & JD Match Percentage</h4>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:

    st.markdown(
        """
        ## Upload Your Resume
        - Supported formats: PDF, DOCX
        - Get insights on your skills and resume score
        """
    )
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF, DOCX)",
        type=["pdf", "docx"]
    )

with col2:

    st.markdown(
        """
        ## Job Description
        - Paste the job description here
        - Only skills will be analyzed
        """
    )
    jd_text = st.text_area("Paste the Job Description here")

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")
    st.write("File Name:", uploaded_file.name)

    file_name = uploaded_file.name.lower()
    text = ""

    try:
        if file_name.endswith(".pdf"):
            # Read PDF
            text = extract_pdf_text(uploaded_file)
        elif file_name.endswith(".docx"):
            # Read DOCX
            text = extract_docx_text(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a PDF or DOCX.")
            st.stop()
    except ValueError as e:
        st.error(f"Failed to read file: {e}")
        st.stop()

    text = text.lower()

    if not text.strip():
        st.warning("Could not extract text from the uploaded file. Please check the file.")
        st.stop()

    if jd_text:
        matched_skills, jd_missing_skills, match_percentage = jd_match(
            text,
            jd_text
        )

        st.subheader("JD Match Percentage")

        st.progress(int(match_percentage))

        st.success(
            f"Match Percentage: {match_percentage:.2f}%"
        )

        st.subheader("Matched Skills")

        if matched_skills:
            for skill in matched_skills:
                st.success(skill)

        st.subheader("Missing JD Skills")

        if jd_missing_skills:
            for skill in jd_missing_skills:
                st.error(skill)

    # Skills list
    found_skills, missing_skills, skills = analyze_skills(text)

    # Found Skills
    st.subheader("Skills Found in Resume")

    if found_skills:
        for skill in found_skills:
            st.success(skill)
    else:
        st.warning("No matching skills found.")

    # Missing Skills
    st.subheader("Skills Missing from Resume")

    if missing_skills:
        for skill in missing_skills:
            st.error(skill)
    else:
        st.success("Great! All listed skills are present.")

    # Resume Score
    score = calculate_score(found_skills, len(skills))

    st.subheader("Resume Score")

    st.progress(int(score))

    st.success(f"Your Resume Score is: {score:.2f}%")

    # Resume Feedback
    st.subheader("Resume Feedback")
    if score >= 80:
        st.success("Excellent! Your resume is well-aligned with the desired skills.")
    elif score >= 50:
        st.warning("Good! Your resume has some of the required skills, but there's room for improvement.")
    else:
        st.error("Needs Improvement. Consider adding more relevant skills to your resume.")