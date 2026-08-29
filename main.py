import json
import os
import webbrowser

from website_scraper import scrape_website
from ollama_analyzer import analyze_website
from report_generator import save_report


def get_urls():
    """
    Ask the user for three website URLs.
    """

    print("=" * 60)
    print("        WEBSITE STRENGTH & WEAKNESS ANALYZER")
    print("                    USING OLLAMA")
    print("=" * 60)
    print()

    urls = []

    for i in range(1, 4):

        while True:

            url = input(
                f"Enter Website {i} URL: "
            ).strip()

            if not url:
                print(
                    "URL cannot be empty. Please try again."
                )
                continue

            # Add https:// if the user did not provide it
            if not url.startswith(
                ("http://", "https://")
            ):
                url = "https://" + url

            urls.append(url)
            break

    return urls


def analyze_websites(urls):
    """
    Scrape and analyze all three websites.
    """

    results = []

    for index, url in enumerate(urls, start=1):

        print()
        print("=" * 60)
        print(f"ANALYZING WEBSITE {index}")
        print("=" * 60)

        print(f"URL: {url}")
        print()

        try:

            print("1/2 Fetching website...")

            website_data = scrape_website(url)

            print(
                "✓ Website scraped successfully."
            )

            print(
                "2/2 Sending website to Ollama..."
            )

            print(
                "   This may take a little while..."
            )

            analysis = analyze_website(
                website_data
            )

            print(
                "✓ AI analysis completed."
            )

            results.append({
                "url": website_data["url"],
                "data": website_data,
                "analysis": analysis,
                "success": True
            })

        except Exception as error:

            print()
            print(
                f"✗ Website {index} failed."
            )

            print(
                f"Reason: {error}"
            )

            results.append({
                "url": url,
                "data": None,
                "analysis": None,
                "success": False,
                "error": str(error)
            })

    return results


def calculate_overall_score(scores):
    """
    Calculate the overall score from the six
    evaluation categories.
    """

    categories = [
        "user_experience",
        "content_quality",
        "navigation",
        "seo",
        "accessibility",
        "trust"
    ]

    total = sum(
        scores[category]
        for category in categories
    )

    return round(
        total / len(categories),
        1
    )


def compare_websites(results):
    """
    Compare successfully analyzed websites.
    """

    successful_results = [
        result
        for result in results
        if result["success"]
        and result["analysis"] is not None
    ]

    if not successful_results:
        return None

    categories = [
        "user_experience",
        "content_quality",
        "navigation",
        "seo",
        "accessibility",
        "trust"
    ]

    comparison = {}

    for category in categories:

        comparison[category] = []

        for result in successful_results:

            score = result["analysis"]["scores"][category]

            comparison[category].append({
                "url": result["url"],
                "score": score
            })

    # Find best overall website
    best_website = max(
        successful_results,
        key=lambda result:
        result["analysis"]["scores"]["overall"]
    )

    # Find weakest website
    weakest_website = min(
        successful_results,
        key=lambda result:
        result["analysis"]["scores"]["overall"]
    )

    # Find strongest individual feature
    strongest_features = []

    for result in successful_results:

        scores = result["analysis"]["scores"]

        best_category = max(
            categories,
            key=lambda category:
            scores[category]
        )

        strongest_features.append({
            "url": result["url"],
            "category": best_category,
            "score": scores[best_category]
        })

    return {
        "category_scores": comparison,

        "best_website": {
            "url": best_website["url"],
            "score": best_website[
                "analysis"
            ]["scores"]["overall"]
        },

        "weakest_website": {
            "url": weakest_website["url"],
            "score": weakest_website[
                "analysis"
            ]["scores"]["overall"]
        },

        "strongest_features": strongest_features
    }


def display_results(results):
    """
    Display individual website analyses.
    """

    print()
    print()
    print("=" * 70)
    print("                         RESULTS")
    print("=" * 70)

    for index, result in enumerate(
        results,
        start=1
    ):

        print()
        print("=" * 70)
        print(f"WEBSITE {index}")
        print("=" * 70)

        print(
            f"\nURL:\n{result['url']}"
        )

        if not result["success"]:

            print("\n✗ Analysis failed.")

            print(
                f"Reason: {result['error']}"
            )

            continue

        analysis = result["analysis"]

        overview = analysis["website_overview"]

        print("\nWEBSITE OVERVIEW")
        print("-" * 70)

        print(
            f"Name: {overview['name']}"
        )

        print(
            f"Purpose: {overview['purpose']}"
        )

        print(
            f"Target Audience: "
            f"{overview['target_audience']}"
        )

        print(
            f"Main Content: "
            f"{overview['main_content']}"
        )

        print("\nSTRENGTHS")
        print("-" * 70)

        for strength in analysis["strengths"]:

            print(
                f"• {strength['point']}"
            )

            print(
                f"  Evidence: "
                f"{strength['evidence']}"
            )

        print("\nWEAKNESSES")
        print("-" * 70)

        for weakness in analysis["weaknesses"]:

            print(
                f"• {weakness['point']}"
            )

            print(
                f"  Evidence: "
                f"{weakness['evidence']}"
            )

        print("\nSCORES")
        print("-" * 70)

        scores = analysis["scores"]

        print(
            f"User Experience: "
            f"{scores['user_experience']}/10"
        )

        print(
            f"Content Quality: "
            f"{scores['content_quality']}/10"
        )

        print(
            f"Navigation: "
            f"{scores['navigation']}/10"
        )

        print(
            f"SEO: "
            f"{scores['seo']}/10"
        )

        print(
            f"Accessibility: "
            f"{scores['accessibility']}/10"
        )

        print(
            f"Trust/Credibility: "
            f"{scores['trust']}/10"
        )

        print(
            f"Overall: "
            f"{scores['overall']}/10"
        )

        print("\nCANNOT BE DETERMINED")
        print("-" * 70)

        for item in analysis[
            "cannot_be_determined"
        ]:

            print(
                f"• {item}"
            )

        print("\nRECOMMENDATIONS")
        print("-" * 70)

        for recommendation in analysis[
            "recommendations"
        ]:

            print(
                f"• {recommendation}"
            )


def display_comparison(
    comparison,
    results
):
    """
    Display the comparison between websites.
    """

    if comparison is None:

        print(
            "\nNo websites were successfully analyzed."
        )

        return

    print()
    print()
    print("=" * 80)
    print("                    WEBSITE COMPARISON")
    print("=" * 80)

    successful_results = [
        result
        for result in results
        if result["success"]
    ]

    websites = [
        result["url"]
        for result in successful_results
    ]

    print()

    header = f"{'Category':<22}"

    for index in range(
        len(websites)
    ):

        header += (
            f"Website {index + 1:<12}"
        )

    print(header)

    print("-" * 80)

    category_names = {
        "user_experience": "User Experience",
        "content_quality": "Content Quality",
        "navigation": "Navigation",
        "seo": "SEO",
        "accessibility": "Accessibility",
        "trust": "Trust/Credibility"
    }

    for category, name in category_names.items():

        row = f"{name:<22}"

        scores = comparison[
            "category_scores"
        ][category]

        for item in scores:

            row += (
                f"{item['score']}/10"
                f"{'':<9}"
            )

        print(row)

    print("-" * 80)

    # Overall scores
    row = f"{'Overall':<22}"

    for result in successful_results:

        score = result[
            "analysis"
        ]["scores"]["overall"]

        row += (
            f"{score}/10"
            f"{'':<9}"
        )

    print(row)

    print()
    print("=" * 80)
    print("                         SUMMARY")
    print("=" * 80)

    best = comparison["best_website"]

    print()
    print("🏆 BEST OVERALL WEBSITE")

    print(
        f"URL: {best['url']}"
    )

    print(
        f"Overall Score: {best['score']}/10"
    )

    print(
        "\nThis website achieved the highest "
        "overall score among the successfully "
        "analyzed websites."
    )

    weakest = comparison["weakest_website"]

    print()
    print("⚠️ WEBSITE WITH LOWEST SCORE")

    print(
        f"URL: {weakest['url']}"
    )

    print(
        f"Overall Score: {weakest['score']}/10"
    )

    print(
        "\nThis website received the lowest "
        "overall score and may benefit most "
        "from improvement."
    )

    print()
    print("💪 STRONGEST FEATURES")

    for feature in comparison[
        "strongest_features"
    ]:

        print(
            f"\n{feature['url']}"
        )

        print(
            f"Best category: "
            f"{feature['category']}"
        )

        print(
            f"Score: {feature['score']}/10"
        )

    print()
    print("=" * 80)

    print(
        "Note: Scores are AI-based preliminary "
        "evaluations based on scraped website "
        "content. They are not professional "
        "website audit measurements."
    )

    print("=" * 80)


def save_json(results, comparison):
    """
    Save all analysis results to a JSON file.
    """

    output = {
        "websites": results,
        "comparison": comparison
    }

    try:

        with open(
            "analysis_results.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                output,
                file,
                indent=4,
                ensure_ascii=False
            )

        print()
        print(
            "✓ Results saved to "
            "analysis_results.json"
        )

        return True

    except Exception as error:

        print(
            f"\nCould not save JSON file: {error}"
        )

        return False


def create_html_report(
    results,
    comparison
):
    """
    Generate the HTML report and open it
    automatically in the default browser.
    """

    try:

        report_file = save_report(
            results,
            comparison
        )

        print()
        print(
            f"✓ HTML report created: "
            f"{report_file}"
        )

        report_path = os.path.abspath(
            report_file
        )

        webbrowser.open(
            "file:///"
            + report_path.replace(
                "\\",
                "/"
            )
        )

        print(
            "✓ Opening report in your browser..."
        )

        return True

    except Exception as error:

        print(
            f"\nCould not create HTML report: "
            f"{error}"
        )

        return False


def main():

    # ---------------------------------------------------------
    # Get URLs
    # ---------------------------------------------------------

    urls = get_urls()

    # ---------------------------------------------------------
    # Analyze websites
    # ---------------------------------------------------------

    results = analyze_websites(
        urls
    )

    # ---------------------------------------------------------
    # Display individual results
    # ---------------------------------------------------------

    display_results(
        results
    )

    # ---------------------------------------------------------
    # Compare websites
    # ---------------------------------------------------------

    print()
    print(
        "Generating comparison..."
    )

    comparison = compare_websites(
        results
    )

    display_comparison(
        comparison,
        results
    )

    # ---------------------------------------------------------
    # Save JSON
    # ---------------------------------------------------------

    save_json(
        results,
        comparison
    )

    # ---------------------------------------------------------
    # Generate HTML report
    # ---------------------------------------------------------

    if comparison is not None:

        create_html_report(
            results,
            comparison
        )

    # ---------------------------------------------------------
    # Finished
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("                 ANALYSIS COMPLETE")
    print("=" * 60)
    print()
    print(
        "Your results are available in:"
    )
    print(
        "  • analysis_results.json"
    )
    print(
        "  • analysis_report.html"
    )
    print()
    print(
        "Thank you for using Website Analyzer!"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()