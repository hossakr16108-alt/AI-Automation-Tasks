import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from google import genai
from google.genai import types

my_key = "YOUR_GEMINI_API_KEY"
client = genai.Client(api_key=my_key)
MODEL_NAME = "gemini-3.6-flash"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

def fetch_website_contents(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else "No title"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        return (title + "\n\n" + text)[:3000]
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def fetch_website_links(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            full_url = urljoin(url, a["href"])
            links.append(full_url)
        return list(set(links))
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, a Company page, or Careers/Jobs pages.
You should respond ONLY in JSON format as in this example:

{
  "links": [
    {"type": "about page", "url": "https://example.com/about"},
    {"type": "careers page", "url": "https://example.com/careers"}
  ]
}
"""

def get_links_user_prompt(url):
    links = fetch_website_links(url)
    user_prompt = f"""
Here is the list of links on the website {url}:
Please decide which of these are relevant web links for a brochure about the company.
Respond with the full HTTPS URL in JSON format.
Do not include Terms of Service, Privacy, or social media links.

Links:
"""
    user_prompt += "\n".join(links[:50])
    return user_prompt

brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors, and recruits.
Respond in Markdown format without code blocks.
Include details of company culture, customers, and careers/jobs if you have the information.
"""

def select_relevant_links(url):
    prompt = get_links_user_prompt(url)
    print(f"Analyzing links for {url}...")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=link_system_prompt,
            response_mime_type="application/json"
        )
    )
    try:
        result = json.loads(response.text)
        return result.get("links", [])
    except json.JSONDecodeError:
        print("Error: Gemini did not return valid JSON.")
        return []

def fetch_page_and_all_relevant_links(url):
    main_page_content = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    combined_content = f"--- MAIN LANDING PAGE ({url}) ---\n{main_page_content}\n\n"
    print(f"Found {len(relevant_links)} relevant links. Fetching their content...")
    for item in relevant_links:
        link_url = item.get("url")
        link_type = item.get("type", "relevant page")
        if link_url:
            sub_content = fetch_website_contents(link_url)
            combined_content += f"--- {link_type.upper()} ({link_url}) ---\n{sub_content}\n\n"
    return combined_content

def create_brochure(company_name, url):
    all_contents = fetch_page_and_all_relevant_links(url)
    print("Generating the final brochure...\n")
    user_prompt = f"""
You are looking at a company called '{company_name}'.
Here are the contents of its landing page and other relevant pages:

{all_contents}

Use this information to build a comprehensive brochure of the company in Markdown.
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=brochure_system_prompt
        )
    )
    return response.text

if __name__ == "__main__":
    company = "Hugging Face"
    target_url = "https://huggingface.co"
    brochure_output = create_brochure(company, target_url)
    print("================ FINAL BROCHURE ================\n")
    print(brochure_output)
