from openai import OpenAI



OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

def comparison_analysis(all_content):
    response = ollama.chat.completions.create(
        model='phi3',
        messages=[
            {'role':'system','content':""" You are an expert market research and competitive analysis assistant. 
Your task is to compare multiple competitor websites based on their features and provide a structured breakdown.

CRITICAL REQUIREMENT:
- You MUST analyze and include EVERY SINGLE website/URL provided in the input context. 
- Do NOT skip, omit, or merge any website, even if its content is brief or incomplete.

For EACH website provided, carefully analyze and compare the following specific features:
1. Core Services / Products: What main offerings do they provide?
2. Target Audience: Who are they selling to (e.g., B2B, B2C, SMBs, Enterprises)?
3. Unique Value Proposition (UVP): What makes them stand out from others?
4. Key Features & Tools: What notable functionalities or tools do they highlight?
5. Pricing & Business Model: Free, freemium, subscription, or quote-based (if mentioned).

Maintain an objective, clear, and professional tone. Structure your output clearly using markdown headers for each company, followed by a final comparison summary."""},
            {'role':'user','content':all_content}
        ]
    ) 
    return response.choices[0].message.content