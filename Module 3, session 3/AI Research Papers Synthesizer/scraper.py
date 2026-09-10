"""
scraper.py
----------
Handles URL validation and web content extraction for the
AI Research Papers Synthesizer.

Pipeline:
    1. urls_filter()          -> validate syntax + reachability
    2. fetch_website_contents() -> scrape a single URL (trafilatura -> BS4 fallback)
    3. get_website_content()  -> aggregate multiple papers into one formatted string
"""

import requests
from urllib.parse import urlparse
import trafilatura
from bs4 import BeautifulSoup

# Standard browser-like User-Agent to avoid basic bot-blocking on academic/doc sites
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

# Character limit per source to keep local LLM context usage manageable
MAX_CHARS = 2500

# Timeout (seconds) for both reachability checks and content fetches
REQUEST_TIMEOUT = 10

# Tags that add noise rather than signal when falling back to BeautifulSoup
TAGS_TO_STRIP = ["script", "style", "img", "input", "nav", "footer", "header", "svg", "noscript"]


def urls_filter(urls_list):
    """
    Validate a list of raw URL strings.

    Checks performed for each URL:
      1. Syntax validity (must have a scheme of http/https and a netloc) via urlparse.
      2. Reachability: a HEAD (falling back to GET) request must return status < 400.

    Args:
        urls_list (list[str]): Raw list of URLs (may contain whitespace/duplicates).

    Returns:
        list[str]: Cleaned list of URLs that are syntactically valid AND reachable.
    """
    valid_urls = []

    for raw_url in urls_list:
        url = raw_url.strip()
        if not url:
            continue

        # --- 1. Syntax validation ---
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            print(f"[urls_filter] Skipping invalid URL syntax: {url}")
            continue

        # --- 2. Reachability check ---
        try:
            # HEAD is cheaper; some servers don't support it well, so fall back to GET
            response = requests.head(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True
            )
            if response.status_code >= 400:
                # Some servers reject HEAD but accept GET — retry before giving up
                response = requests.get(
                    url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True, stream=True
                )

            if response.status_code < 400:
                valid_urls.append(url)
            else:
                print(f"[urls_filter] Unreachable ({response.status_code}): {url}")

        except requests.RequestException as e:
            print(f"[urls_filter] Request failed for {url}: {e}")
            continue

    return valid_urls


def fetch_website_contents(url):
    """
    Fetch and extract the main textual content of a single URL.

    Strategy:
      1. Download the raw HTML with a standard User-Agent.
      2. Attempt extraction via trafilatura (best for articles/papers, strips
         boilerplate automatically).
      3. If trafilatura fails (returns None), fall back to a manual
         BeautifulSoup extraction that strips out irrelevant tags.
      4. Truncate the result to MAX_CHARS to respect local LLM context limits.

    Args:
        url (str): A single, pre-validated URL.

    Returns:
        str: Extracted (and truncated) text content. Empty string on failure.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[fetch_website_contents] Failed to fetch {url}: {e}")
        return ""

    text_content = None

    # --- Primary extraction: trafilatura ---
    try:
        text_content = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=False,
        )
    except Exception as e:
        print(f"[fetch_website_contents] trafilatura error on {url}: {e}")
        text_content = None

    # --- Fallback extraction: BeautifulSoup ---
    if not text_content:
        print(f"[fetch_website_contents] trafilatura returned None for {url}, using BS4 fallback.")
        try:
            soup = BeautifulSoup(response.text, "html.parser")

            # Strip irrelevant / noisy tags before extracting text
            for tag in soup(TAGS_TO_STRIP):
                tag.decompose()

            # get_text with a separator keeps paragraphs from running together
            raw_text = soup.get_text(separator="\n")

            # Collapse excessive blank lines/whitespace
            lines = [line.strip() for line in raw_text.splitlines()]
            text_content = "\n".join(line for line in lines if line)

        except Exception as e:
            print(f"[fetch_website_contents] BS4 fallback failed for {url}: {e}")
            text_content = ""

    if not text_content:
        return ""

    # --- Truncate to protect local LLM context window ---
    return text_content[:MAX_CHARS]


def get_website_content(valid_urls):
    """
    Iterate over validated URLs, fetch each one's content, and aggregate
    everything into a single clearly-delimited string ready to hand off
    to the AI synthesis engine.

    Args:
        valid_urls (list[str]): URLs that have already passed urls_filter().

    Returns:
        str: Aggregated, labeled content for all successfully scraped papers.
             Returns an empty string if nothing could be scraped.
    """
    aggregated_sections = []

    for index, url in enumerate(valid_urls, start=1):
        print(f"[get_website_content] Fetching paper {index}/{len(valid_urls)}: {url}")
        content = fetch_website_contents(url)

        if not content:
            # Still note the failure so the LLM (and user) knows a source was skipped
            section = (
                f"--- PAPER {index} ---\n"
                f"SOURCE URL: {url}\n"
                f"STATUS: Failed to retrieve content.\n"
            )
        else:
            section = (
                f"--- PAPER {index} ---\n"
                f"SOURCE URL: {url}\n"
                f"CONTENT:\n{content}\n"
            )

        aggregated_sections.append(section)

    return "\n\n".join(aggregated_sections)
