import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from openai import OpenAI


# Connect to Ollama
ollama = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# Ask for website URL
url = input("Enter website URL: ")


# Get main website
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")


# Extract links
links = []

for link in soup.find_all("a", href=True):
    full_url = urljoin(url, link["href"])

    if full_url.startswith("http"):
        links.append(full_url)


# Remove duplicates
links = list(set(links))


print(f"\nFound {len(links)} links.")


# Take first 20 links
links = links[:20]

links_text = "\n".join(links)


print("\nSending links to Ollama...")


# Ask Ollama to select important links
ai_response = ollama.chat.completions.create(
    model="qwen-local:latest",
    messages=[
        {
            "role": "system",
            "content": """
You are a website analysis assistant.

Look at the provided website links and identify the most important
professional links.

Choose links related to:
About, Company, Projects, Experience, Careers, Services, or Products.

Return ONLY the URLs.
Put each URL on a separate line.
Do not use Markdown.
Do not use JSON.
Do not explain anything.
"""
        },
        {
            "role": "user",
            "content": f"""
Website:
{url}

Links:
{links_text}
"""
        }
    ]
)


# Get AI result
selected_links_text = ai_response.choices[0].message.content


print("\nImportant Links Selected By AI:\n")

print(selected_links_text)


# Convert AI response into a list
selected_links = []

for line in selected_links_text.splitlines():

    line = line.strip()

    if line.startswith("http://") or line.startswith("https://"):
        selected_links.append(line)


print("\n\nFetching selected pages...\n")


# Fetch the content of each selected page
for selected_url in selected_links:

    try:

        page_response = requests.get(
            selected_url,
            timeout=10
        )

        page_soup = BeautifulSoup(
            page_response.text,
            "html.parser"
        )

        page_text = page_soup.get_text(
            separator=" ",
            strip=True
        )

        print("=" * 60)

        print("URL:")
        print(selected_url)

        print("\nPage Content:")

        print(page_text[:1000])

        print()

    except Exception as e:

        print("Could not fetch:")
        print(selected_url)

        print("Error:", e)