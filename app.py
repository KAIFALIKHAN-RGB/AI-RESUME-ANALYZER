import streamlit as st
from resume.pdf_reader import extract_pdf_text
from resume.docx_reader import extract_docx_text

from analyzer.skill_matcher import analyze_skills
from analyzer.scorer import calculate_score
from analyzer.jd_matcher import jd_match
from utils.gemini_feedback import get_resume_feedback


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
            col1, col2 = st.columns(2)
            for i, skill in enumerate(matched_skills):
                if i % 2 == 0:
                    with col1:
                        st.success(skill)
                else:
                    with col2:
                        st.success(skill)

        st.subheader("Missing JD Skills")

        if jd_missing_skills:
            for skill in jd_missing_skills:
                st.error(skill)

        else:
            st.success("🥳Great! All JD skills are present in your resume.")

        # ===== Gemini AI Feedback =====

        st.subheader("🤖 Gemini AI Feedback")

        with st.spinner("Analyzing Resume with Gemini AI..."):
          try:
             feedback = get_resume_feedback(
                text,
                jd_text
            )
          except Exception as e:
             st.error(f"Error getting feedback from Gemini AI: {e}")
             feedback = "Unable to retrieve feedback at this time."

        with st.expander("View Gemini AI Feedback"):
         st.markdown(feedback)

    # Skills list
    found_skills, missing_skills, skills = analyze_skills(text)
    total_skills = len(skills)
    score = calculate_score(found_skills, total_skills)

    st.subheader("📊 Resume Metrics Dashboard")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Resume Score", f"{score:.2f}%")
    metric_cols[1].metric("Found Skills", len(found_skills), f"of {total_skills}")
    metric_cols[2].metric("Missing Skills", len(missing_skills))
    if jd_text:
        metric_cols[3].metric("JD Match", f"{match_percentage:.2f}%", f"{len(matched_skills)} skills matched")
    else:
        metric_cols[3].metric("JD Match", "N/A", "Add a job description")

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

    st.subheader("📜 Resume Score")
    st.progress(int(score))
    st.success(f"Your Resume Score is: {score:.2f}%")

    # Resume Feedback
    st.subheader("💡 Resume Recommendation")
    if score >= 80:
        st.success("Excellent! Your resume is well-aligned with the desired skills.")
        st.balloons()
    elif score >= 50:
        st.warning("Good! Your resume has some of the required skills, but there's room for improvement.")
    else:
        feedback = get_resume_feedback(text, jd_text)
        st.error("Needs Improvement. Consider adding more relevant skills to your resume.")
        st.text_area("Feedback:", value=feedback, height=200)