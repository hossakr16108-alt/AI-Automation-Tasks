import streamlit as st
from ai_engine import (
    resume_analysis, 
    match_resume_to_job, 
    fetch_full_portfolio_content
)

st.set_page_config(page_title="AI Resume & Portfolio Matcher", layout="wide")

st.title("AI Resume & Portfolio Matcher")
st.write("Match candidate profiles or portfolios against job requirements.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Candidate Resume / Portfolio")
    
    input_type = st.radio(
        "Select Resume Input Type:",
        ("Portfolio / Website URL", "Raw Text", "Upload File (PDF/DOCX)")
    )
    
    cv_content = ""
    
    if input_type == "Portfolio / Website URL":
        portfolio_url = st.text_input("Enter Portfolio URL:", placeholder="https://my-portfolio.com")
        
    elif input_type == "Raw Text":
        cv_content = st.text_area("Paste Resume Text:", height=250)
        
    elif input_type == "Upload File (PDF/DOCX)":
        uploaded_file = st.file_uploader("Upload CV File", type=["pdf", "docx", "txt"])
        if uploaded_file is not None:
            cv_content = uploaded_file.read().decode("utf-8", errors="ignore")
            st.success("File uploaded successfully!")

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area(
        "Paste Job Description Text Here:", 
        height=320, 
        placeholder="We are looking for a Software Engineer with Python skills..."
    )

st.markdown("---")

if st.button("Analyze and Match", type="primary"):
    if not job_description.strip():
        st.error("Please provide a Job Description!")
    else:
        with st.status("Processing Candidate Data...", expanded=True) as status:
            extracted_text = ""
            
            # Step 1: Content Extraction
            st.write("Scraping and reading content...")
            if input_type == "Portfolio / Website URL":
                if portfolio_url:
                    extracted_text = fetch_full_portfolio_content(portfolio_url)
                else:
                    st.error("Please enter a valid URL!")
                    st.stop()
            elif input_type in ["Raw Text", "Upload File (PDF/DOCX)"]:
                extracted_text = cv_content

            if extracted_text:
                # Step 2: Structured Data Extraction (Pass 1)
                st.write("Extracting structured JSON profile (Pass 1)...")
                parsed_resume = resume_analysis(extracted_text)
                
                # Step 3: Match Report Generation (Pass 2)
                st.write("Generating job matching report (Pass 2)...")
                matching_report = match_resume_to_job(parsed_resume, job_description)
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                # Display Output
                st.success("Analysis Complete!")
                st.subheader("Matching Analysis Report")
                st.markdown(matching_report)
            else:
                st.error("No text could be extracted from the provided input!")
