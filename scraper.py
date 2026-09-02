"""
scraper.py

Fetches REAL product data from https://webscraper.io/test-sites/e-commerce/allinone
This is a public sandbox site built specifically for practicing web scraping
(no login, no rate limiting, stable HTML structure), so it's safe to hit
repeatedly while building/testing a pipeline like this one.

Swap CATEGORY_URLS for a different real store's URLs + selectors if you want
to point this at an actual production site later — the rest of the pipeline
doesn't need to change, since every downstream step just consumes the list
of dicts this file returns.
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

CATEGORY_URLS = {
    "laptops": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
    "tablets": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
    "phones": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch",
}


def fetch_products_by_category(category: str, timeout: int = 10) -> list[dict]:
    """
    REAL web fetch — hits the live site and parses the current product listing.

    Returns a list of dicts:
        {"name": str, "price": float, "description": str,
         "reviews": int, "url": str}
    """
    category = category.lower().strip()
    if category not in CATEGORY_URLS:
        raise ValueError(
            f"Unknown category '{category}'. Choose one of: {list(CATEGORY_URLS)}"
        )

    url = CATEGORY_URLS[category]
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for card in soup.select("div.product-wrapper"):
        title_tag = card.select_one("a.title")
        price_tag = card.select_one("h4.price")
        desc_tag = card.select_one("p.description")
        reviews_tag = card.select_one("p.review-count")

        if not title_tag or not price_tag:
            continue  # skip anything that doesn't look like a real product card

        # the <a class="title"> text is often truncated with "...";
        # the full name lives in its "title" attribute when present
        name = title_tag.get("title", "").strip() or title_tag.get_text(strip=True)

        price_text = price_tag.get_text(strip=True).replace("$", "").replace(",", "")
        try:
            price = float(price_text)
        except ValueError:
            price = None

        reviews_text = reviews_tag.get_text(strip=True) if reviews_tag else "0"
        reviews = int("".join(ch for ch in reviews_text if ch.isdigit()) or 0)

        href = title_tag.get("href", "")
        full_url = href if href.startswith("http") else f"https://webscraper.io{href}"

        products.append({
            "name": name,
            "price": price,
            "description": desc_tag.get_text(strip=True) if desc_tag else "",
            "reviews": reviews,
            "url": full_url,
        })

    return products
