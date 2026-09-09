from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# Connect to Ollama
OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

# Browser-like headers
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


def fetch_website_contents(url):
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )

    # Get page title
    if soup.title:
        title = soup.title.get_text(strip=True)
    else:
        title = "No title"

    # Get clean text
    if soup.body:
        for irrelevant in soup.body(
            ["script", "style", "img", "input", "noscript"]
        ):
            irrelevant.decompose()

        text = soup.body.get_text(
            separator="\n",
            strip=True
        )
    else:
        text = ""

    # Limit the amount of text
    return (title + "\n\n" + text)[:2000]


# AI websites
url1 = "https://en.wikipedia.org/wiki/Artificial_intelligence"
url2 = "https://en.wikipedia.org/wiki/Machine_learning"
url3 = "https://en.wikipedia.org/wiki/Deep_learning"


print("Fetching AI website data...\n")


data1 = fetch_website_contents(url1)
print("✓ Artificial Intelligence website fetched")

data2 = fetch_website_contents(url2)
print("✓ Machine Learning website fetched")

data3 = fetch_website_contents(url3)
print("✓ Deep Learning website fetched")


# Combine all website data
all_data = f"""
--- ARTIFICIAL INTELLIGENCE DATA ---

{data1}


--- MACHINE LEARNING DATA ---

{data2}


--- DEEP LEARNING DATA ---

{data3}
"""


# Prompt for Qwen
prompt = f"""
You are an AI assistant specialized in analyzing AI-related website content.

Analyze the following website data.

Your tasks are:

1. Summarize the main information about Artificial Intelligence.
2. Summarize the main information about Machine Learning.
3. Summarize the main information about Deep Learning.
4. Create a clear comparison table in Markdown.
5. Explain the relationship between AI, Machine Learning, and Deep Learning.
6. Mention the important similarities and differences.
7. Compare the three topics based ONLY on the provided data.
8. Do not invent information that is not present in the provided data.
9. Make the answer clear and easy to understand.

Website data:

{all_data}
"""


print("\nSending data to Qwen...\n")


# Send data to Qwen through Ollama
response = ollama.chat.completions.create(
    model="qwen-local:latest",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant "
                "specialized in AI concepts and website analysis."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# Display result
print("\n")
print("=" * 60)
print("AI ANALYSIS")
print("=" * 60)

print(response.choices[0].message.content)

print("=" * 60)