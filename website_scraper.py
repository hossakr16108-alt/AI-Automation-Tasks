import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

MAX_TEXT_LENGTH = 12000
MAX_LINKS = 100


def normalize_url(url):
    """
    Add https:// if the user did not provide a protocol.
    """

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def validate_url(url):
    """
    Check whether the URL has a valid HTTP/HTTPS structure.
    """

    url = normalize_url(url)

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            "URL must use HTTP or HTTPS."
        )

    if not parsed.netloc:
        raise ValueError(
            "The URL does not contain a valid website domain."
        )

    return url


def scrape_website(url):
    """
    Fetch a website and extract useful information from its HTML.

    Returns a dictionary containing:
    - URL
    - Title
    - Meta description
    - Headings
    - Visible text
    - Links
    - Basic HTML information
    """

    # ---------------------------------------------------------
    # Validate and normalize URL
    # ---------------------------------------------------------

    url = validate_url(url)

    # ---------------------------------------------------------
    # Fetch website
    # ---------------------------------------------------------

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise Exception(
            "The website took too long to respond."
        )

    except requests.exceptions.ConnectionError:
        raise Exception(
            "Could not connect to the website. "
            "Check the URL and your internet connection."
        )

    except requests.exceptions.HTTPError:
        status_code = response.status_code

        if status_code == 403:
            raise Exception(
                "Access denied by the website (HTTP 403)."
            )

        elif status_code == 404:
            raise Exception(
                "The webpage was not found (HTTP 404)."
            )

        elif status_code >= 500:
            raise Exception(
                f"The website server returned an error "
                f"(HTTP {status_code})."
            )

        else:
            raise Exception(
                f"The website returned HTTP {status_code}."
            )

    except requests.exceptions.RequestException as error:
        raise Exception(
            f"Could not fetch the website: {error}"
        )

    # ---------------------------------------------------------
    # Check that the response contains HTML
    # ---------------------------------------------------------

    content_type = response.headers.get(
        "Content-Type",
        ""
    )

    if "text/html" not in content_type.lower():
        raise Exception(
            "The URL does not appear to contain an HTML webpage."
        )

    # ---------------------------------------------------------
    # Parse HTML
    # ---------------------------------------------------------

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Check for empty HTML
    if not soup.get_text(strip=True) and not soup.find():
        raise Exception(
            "The webpage returned empty HTML."
        )

    # ---------------------------------------------------------
    # Remove unnecessary elements
    # ---------------------------------------------------------

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    # ---------------------------------------------------------
    # Extract title
    # ---------------------------------------------------------

    title = ""

    if soup.title:
        title = soup.title.get_text(strip=True)

    # ---------------------------------------------------------
    # Extract meta description
    # ---------------------------------------------------------

    meta_description = ""

    meta_tag = soup.find(
        "meta",
        attrs={
            "name": lambda value:
                value and value.lower() == "description"
        }
    )

    if meta_tag:
        meta_description = meta_tag.get(
            "content",
            ""
        ).strip()

    # ---------------------------------------------------------
    # Extract headings
    # ---------------------------------------------------------

    headings = []

    for heading in soup.find_all(
        ["h1", "h2", "h3"]
    ):
        text = heading.get_text(
            " ",
            strip=True
        )

        if text:
            headings.append(text)

    # ---------------------------------------------------------
    # Extract visible text
    # ---------------------------------------------------------

    visible_text = soup.get_text(
        " ",
        strip=True
    )

    visible_text = " ".join(
        visible_text.split()
    )

    # Limit text sent to Ollama.
    visible_text = visible_text[
        :MAX_TEXT_LENGTH
    ]

    # ---------------------------------------------------------
    # Extract links
    # ---------------------------------------------------------

    links = []

    for link in soup.find_all(
        "a",
        href=True
    ):
        href = link.get("href")

        if not href:
            continue

        absolute_url = urljoin(
            url,
            href
        )

        link_text = link.get_text(
            " ",
            strip=True
        )

        links.append({
            "text": link_text,
            "url": absolute_url
        })

    links = links[:MAX_LINKS]

    # ---------------------------------------------------------
    # Basic HTML structure
    # ---------------------------------------------------------

    html_tag = soup.find("html")

    language = ""

    if html_tag:
        language = html_tag.get(
            "lang",
            ""
        )

    images = soup.find_all("img")

    images_with_alt = sum(
        1
        for image in images
        if image.get("alt")
    )

    basic_structure = {
        "language": language,
        "number_of_images": len(images),
        "images_with_alt_text": images_with_alt,
        "number_of_headings": len(headings),
        "number_of_links": len(links),
    }

    # ---------------------------------------------------------
    # Return structured website data
    # ---------------------------------------------------------

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "visible_text": visible_text,
        "links": links,
        "basic_structure": basic_structure,
    }


# -------------------------------------------------------------
# TESTING
# -------------------------------------------------------------

if __name__ == "__main__":

    test_url = "https://example.com"

    try:
        website = scrape_website(test_url)

        print("=" * 60)
        print("WEBSITE SCRAPER TEST")
        print("=" * 60)

        print(f"\nURL:")
        print(website["url"])

        print(f"\nTitle:")
        print(website["title"])

        print(f"\nMeta Description:")
        print(website["meta_description"])

        print("\nHeadings:")

        for heading in website["headings"]:
            print(f"- {heading}")

        print("\nBasic Structure:")
        print(website["basic_structure"])

        print("\nVisible Text:")
        print(
            website["visible_text"][:1000]
        )

        print("\nNumber of Links:")
        print(
            len(website["links"])
        )

        print("\n" + "=" * 60)
        print("SCRAPING SUCCESSFUL!")
        print("=" * 60)

    except Exception as error:
        print("\nSCRAPING FAILED")
        print(f"Reason: {error}")