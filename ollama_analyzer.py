import json
import requests

from prompts import create_website_analysis_prompt


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def calculate_overall_score(scores):
    """
    Calculate the overall score using Python.

    The overall score is the average of the
    six main evaluation categories.
    """

    categories = [
        "user_experience",
        "content_quality",
        "navigation",
        "seo",
        "accessibility",
        "trust"
    ]

    values = [
        scores[category]
        for category in categories
    ]

    return round(
        sum(values) / len(values),
        1
    )


def analyze_website(website_data):
    """
    Send website data to Ollama and return
    structured analysis.
    """

    prompt = create_website_analysis_prompt(
        website_data
    )

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        if "response" not in result:
            raise Exception(
                "Ollama returned a response without AI text."
            )

        raw_analysis = result["response"]

        try:
            analysis = json.loads(
                raw_analysis
            )

        except json.JSONDecodeError:
            raise Exception(
                "Ollama returned invalid JSON."
            )

        # -----------------------------------------------------
        # Validate required fields
        # -----------------------------------------------------

        required_fields = [
            "website_overview",
            "strengths",
            "weaknesses",
            "scores",
            "cannot_be_determined",
            "recommendations"
        ]

        for field in required_fields:

            if field not in analysis:
                raise Exception(
                    f"Ollama response is missing: {field}"
                )

        scores = analysis["scores"]

        score_categories = [
            "user_experience",
            "content_quality",
            "navigation",
            "seo",
            "accessibility",
            "trust"
        ]

        for category in score_categories:

            if category not in scores:
                raise Exception(
                    f"Missing score: {category}"
                )

            score = scores[category]

            if not isinstance(score, int):
                raise Exception(
                    f"Score for {category} must be an integer."
                )

            if not 1 <= score <= 10:
                raise Exception(
                    f"Score for {category} must be between 1 and 10."
                )

        # -----------------------------------------------------
        # Calculate overall score
        # -----------------------------------------------------

        analysis["scores"]["overall"] = (
            calculate_overall_score(scores)
        )

        return analysis

    except requests.exceptions.ConnectionError:
        raise Exception(
            "Could not connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise Exception(
            "Ollama took too long to respond."
        )

    except requests.exceptions.HTTPError:
        raise Exception(
            f"Ollama returned HTTP {response.status_code}."
        )

    except requests.exceptions.RequestException as error:
        raise Exception(
            f"Could not communicate with Ollama: {error}"
        )


# -------------------------------------------------------------
# TESTING
# -------------------------------------------------------------

if __name__ == "__main__":

    from website_scraper import scrape_website

    print("=" * 60)
    print("STRUCTURED WEBSITE ANALYSIS TEST")
    print("=" * 60)

    try:

        print("\n1. Scraping website...")

        website = scrape_website(
            "https://example.com"
        )

        print(
            "   Scraping successful!"
        )

        print("\n2. Sending data to Ollama...")

        analysis = analyze_website(
            website
        )

        print(
            "   Ollama analysis successful!"
        )

        print("\n3. Parsed analysis:")

        print(
            json.dumps(
                analysis,
                indent=4,
                ensure_ascii=False
            )
        )

        print("\n" + "=" * 60)
        print("STRUCTURED ANALYSIS SUCCESSFUL!")
        print("=" * 60)

    except Exception as error:

        print("\nERROR:")
        print(error)