from google import genai
import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. Gemini API Key and Client
# =========================================================

my_key = "AQ.Ab8RN6J7KnAZ0AjffCQUsxtrmBS7L7wytntIGrDAPHyyTv2f4w"

client = genai.Client(api_key=my_key)


# =========================================================
# 2. Website headers
# =========================================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


# =========================================================
# 3. Function to fetch website contents
# =========================================================

def fetch_website_contents(url):

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    # Check if the request was successful
    response.raise_for_status()

    # Convert HTML into a BeautifulSoup object
    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )

    # Get website title
    title = (
        soup.title.string
        if soup.title
        else "No title"
    )

    # Remove unnecessary elements
    if soup.body:

        for irrelevant in soup.body(
            ["script", "style", "img", "input"]
        ):
            irrelevant.decompose()

        # Extract text from the body
        text = soup.body.get_text(
            separator="\n",
            strip=True
        )

    else:
        text = ""

    # Return title + website text
    # Limit each website to 2000 characters
    return (
        title + "\n\n" + text
    )[:2000]


# =========================================================
# 4. URLs of the three websites
# =========================================================

url1 = "https://en.wikipedia.org/wiki/Fish"

url2 = "https://en.wikipedia.org/wiki/Salmon"

url3 = "https://en.wikipedia.org/wiki/Aquarium"


# =========================================================
# 5. Fetch data from the three websites
# =========================================================

data1 = fetch_website_contents(url1)

data2 = fetch_website_contents(url2)

data3 = fetch_website_contents(url3)


# =========================================================
# 6. Combine all website data
# =========================================================

all_data = f"""
--- FISH DATA ---

{data1}


--- SALMON DATA ---

{data2}


--- AQUARIUM DATA ---

{data3}
"""


# =========================================================
# 7. Create the prompt for Gemini
# =========================================================

prompt = f"""
Please analyze the following website data.

Your tasks are:

1. Summarize the main information from each website.
2. Create a clear comparison table in Markdown.
3. Compare the topics based only on the provided data.
4. Make the answer clear and easy to understand.

The website data is:

{all_data}
"""


# =========================================================
# 8. Send the data to Gemini
# =========================================================

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


# =========================================================
# 9. Print Gemini's response
# =========================================================

print(response.text)
