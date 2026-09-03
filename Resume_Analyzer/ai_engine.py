from openai import OpenAI
import json
from scraper import fetch_website_links, fetch_website_contents
 
OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')


system_prompt = """You are an expert HR Data Extractor and Resume Analyzer.
Your task is to analyze the provided candidate Resume and extract all key professional details. CRITICAL REQUIREMENT:
You MUST respond ONLY with a single, valid JSON object. Do NOT include any intro text, markdown formatting (like ```json), explanations, or notes.
### EXAMPLE INPUT:John Doe is a Junior Software Developer with skills in Python and SQL. He built a Weather App using Flask and Python. He studied Computer Science at Cairo University.
### EXAMPLE OUTPUT:
{
  "candidate_info": {
    "name": "John Doe",
    "current_title": "Junior Software Developer",
    "experience_level": "Entry-level"
  },
  "technical_skills": ["Python", "SQL", "Flask"],
  "soft_skills": [],
  "projects": [
    {
      "title": "Weather App",
      "description": "Built a weather application",
      "technologies_used": ["Flask", "Python"]
    }
  ],
  "work_experience": [],
  "education": [
    {
      "degree": "Computer Science",
      "institution": "Cairo University"
    }  ]}
### ACTUAL INPUT TO PROCESS:
[Here goes the actual resume text]
"""

def resume_analysis(resume_text):
    response = ollama.chat.completions.create(
        model='llama3.1:8b',
        
        response_format={"type": "json_object"},     
        messages=[
            {'role': 'system', 'content': system_prompt },
            {'role': 'user', 'content': resume_text }
        ]
    )
    parsed_json = json.loads(response.choices[0].message.content)   
    return parsed_json 

portfolio_link_system_prompt = """
You are an AI Assistant specialized in analyzing Portfolio Websites.
Select ONLY the links that contain core professional data (Projects, Case Studies, Work Experience, or Skills).
Exclude social media, terms of service, and login links.

You MUST respond strictly with a JSON object:
{
  "links": [
    {"type": "project / about / experience", "url": "https://full.url/goes/here"}
  ]
}
"""
def extract_relevant_portfolio_links(portfolio_url):
    raw_links = fetch_website_links(portfolio_url)
    user_prompt = f"Portfolio Base URL: {portfolio_url}\nLinks found:\n" + "\n".join(raw_links)
    
    response = ollama.chat.completions.create(
        model='llama3.1:8b',
        response_format={"type": "json_object"},  # Replace format='json' with this
        messages=[
            {'role': 'system', 'content': portfolio_link_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    )
    return json.loads(response.choices[0].message.content)

def fetch_full_portfolio_content(portfolio_url):
    links_json = extract_relevant_portfolio_links(portfolio_url)
    
    full_content = f"--- Main Portfolio Page ---\n{fetch_website_contents(portfolio_url)}\n\n"
    
    if "links" in links_json:
        for item in links_json["links"]:
            link_url = item.get("url")
            if link_url:
                page_content = fetch_website_contents(link_url)
                full_content += f"--- Page Content from {link_url} ---\n{page_content}\n\n"
                
    return full_content

system_prompt_match = """You are an expert Technical Recruiter and Career Advisor.

Your task is to analyze a candidate's structured resume data (provided in JSON format) and compare it against a Job Description text to evaluate their fit for the role.

Evaluate the following key areas:
1. Skills Alignment: Match the candidate's technical and soft skills against the job requirements.
2. Experience & Project Relevance: Assess whether the candidate's past projects and experience demonstrate the capabilities required for this job.
3. Gap Analysis: Identify critical missing skills or qualifications that the candidate lacks.

Output Requirements:
Provide a clear, structured report with the following sections:
- Overall Match Percentage (0-100%)
- Core Strengths & Matching Qualifications
- Missing Requirements & Skill Gaps
- Actionable Recommendations (How the candidate can bridge the gaps)

Keep your tone professional, objective, and constructive.
"""

def match_resume_to_job(parsed_json, job_description_text):
     user_input = f"""
Candidate Structured Profile (JSON):
{json.dumps(parsed_json, ensure_ascii=False)}

Job Description Text:
{job_description_text}
"""  
     response = ollama.chat.completions.create(
       
        model='llama3.1:8b',
        messages=[
            {'role': 'system', 'content': system_prompt_match },
            {'role': 'user', 'content': user_input }
        ]
    )
        
     return response.choices[0].message.content 
 