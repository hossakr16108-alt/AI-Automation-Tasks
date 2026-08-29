import html


def escape(value):
    """
    Safely convert text into HTML.
    """
    return html.escape(str(value))


def generate_report(results, comparison):
    """
    Generate a professional HTML report.
    """

    successful_results = [
        result
        for result in results
        if result["success"]
    ]

    website_sections = ""

    for index, result in enumerate(
        successful_results,
        start=1
    ):

        analysis = result["analysis"]
        overview = analysis["website_overview"]
        scores = analysis["scores"]

        strengths_html = ""

        for strength in analysis["strengths"]:

            strengths_html += f"""
            <li>
                <strong>{escape(strength["point"])}</strong>
                <br>
                <span>{escape(strength["evidence"])}</span>
            </li>
            """

        weaknesses_html = ""

        for weakness in analysis["weaknesses"]:

            weaknesses_html += f"""
            <li>
                <strong>{escape(weakness["point"])}</strong>
                <br>
                <span>{escape(weakness["evidence"])}</span>
            </li>
            """

        recommendations_html = ""

        for recommendation in analysis[
            "recommendations"
        ]:

            recommendations_html += f"""
            <li>{escape(recommendation)}</li>
            """

        cannot_determine_html = ""

        for item in analysis[
            "cannot_be_determined"
        ]:

            cannot_determine_html += f"""
            <li>{escape(item)}</li>
            """

        website_sections += f"""
        <section class="website-card">

            <div class="website-header">
                <h2>Website {index}</h2>

                <a href="{escape(result["url"])}"
                   target="_blank">
                    {escape(result["url"])}
                </a>
            </div>

            <div class="overview">

                <h3>Website Overview</h3>

                <p>
                    <strong>Name:</strong>
                    {escape(overview["name"])}
                </p>

                <p>
                    <strong>Purpose:</strong>
                    {escape(overview["purpose"])}
                </p>

                <p>
                    <strong>Target Audience:</strong>
                    {escape(overview["target_audience"])}
                </p>

                <p>
                    <strong>Main Content:</strong>
                    {escape(overview["main_content"])}
                </p>

            </div>

            <div class="scores">

                <h3>Scores</h3>

                <div class="score-grid">

                    <div class="score">
                        <span>User Experience</span>
                        <strong>
                            {scores["user_experience"]}/10
                        </strong>
                    </div>

                    <div class="score">
                        <span>Content Quality</span>
                        <strong>
                            {scores["content_quality"]}/10
                        </strong>
                    </div>

                    <div class="score">
                        <span>Navigation</span>
                        <strong>
                            {scores["navigation"]}/10
                        </strong>
                    </div>

                    <div class="score">
                        <span>SEO</span>
                        <strong>
                            {scores["seo"]}/10
                        </strong>
                    </div>

                    <div class="score">
                        <span>Accessibility</span>
                        <strong>
                            {scores["accessibility"]}/10
                        </strong>
                    </div>

                    <div class="score">
                        <span>Trust / Credibility</span>
                        <strong>
                            {scores["trust"]}/10
                        </strong>
                    </div>

                    <div class="score overall">
                        <span>Overall</span>
                        <strong>
                            {scores["overall"]}/10
                        </strong>
                    </div>

                </div>

            </div>

            <div class="two-columns">

                <div class="strengths">

                    <h3>💪 Strengths</h3>

                    <ul>
                        {strengths_html}
                    </ul>

                </div>

                <div class="weaknesses">

                    <h3>⚠️ Weaknesses</h3>

                    <ul>
                        {weaknesses_html}
                    </ul>

                </div>

            </div>

            <div class="recommendations">

                <h3>💡 Recommendations</h3>

                <ul>
                    {recommendations_html}
                </ul>

            </div>

            <div class="limitations">

                <h3>❓ Cannot Be Determined</h3>

                <ul>
                    {cannot_determine_html}
                </ul>

            </div>

        </section>
        """

    # ---------------------------------------------------------
    # Comparison
    # ---------------------------------------------------------

    best = comparison["best_website"]

    weakest = comparison["weakest_website"]

    comparison_rows = ""

    category_names = {
        "user_experience": "User Experience",
        "content_quality": "Content Quality",
        "navigation": "Navigation",
        "seo": "SEO",
        "accessibility": "Accessibility",
        "trust": "Trust / Credibility"
    }

    for category, name in category_names.items():

        values = comparison[
            "category_scores"
        ][category]

        cells = ""

        for item in values:

            cells += f"""
            <td>{item["score"]}/10</td>
            """

        comparison_rows += f"""
        <tr>
            <th>{escape(name)}</th>
            {cells}
        </tr>
        """

    # ---------------------------------------------------------
    # Website names for table
    # ---------------------------------------------------------

    headers = ""

    for index, result in enumerate(
        successful_results,
        start=1
    ):

        headers += f"""
        <th>Website {index}</th>
        """

    # ---------------------------------------------------------
    # Complete HTML
    # ---------------------------------------------------------

    html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Website Strength & Weakness Analyzer
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f3f7;
    color: #29242e;
    line-height: 1.6;
}}

.container {{
    width: 90%;
    max-width: 1200px;
    margin: auto;
}}

header {{
    background: #2d2433;
    color: white;
    padding: 50px 20px;
    text-align: center;
}}

header h1 {{
    margin: 0;
    font-size: 36px;
}}

header p {{
    margin-top: 10px;
    opacity: 0.85;
}}

.summary {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin: 35px 0;
}}

.summary-card {{
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow:
        0 3px 12px rgba(0,0,0,0.08);
}}

.summary-card h3 {{
    margin-top: 0;
}}

.summary-card .score {{
    font-size: 28px;
    font-weight: bold;
}}

.comparison {{
    background: white;
    padding: 30px;
    border-radius: 14px;
    margin-bottom: 35px;
    box-shadow:
        0 3px 12px rgba(0,0,0,0.08);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 14px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}}

th:first-child {{
    text-align: left;
}}

.website-card {{
    background: white;
    padding: 35px;
    margin-bottom: 35px;
    border-radius: 14px;
    box-shadow:
        0 3px 12px rgba(0,0,0,0.08);
}}

.website-header {{
    border-bottom: 1px solid #ddd;
    padding-bottom: 20px;
    margin-bottom: 25px;
}}

.website-header h2 {{
    margin-bottom: 5px;
}}

.website-header a {{
    word-break: break-all;
}}

h3 {{
    margin-top: 25px;
}}

.score-grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
}}

.score {{
    background: #f5f3f7;
    padding: 18px;
    border-radius: 10px;
    text-align: center;
}}

.score span {{
    display: block;
    font-size: 14px;
}}

.score strong {{
    display: block;
    font-size: 24px;
    margin-top: 5px;
}}

.score.overall {{
    background: #e8dff0;
}}

.two-columns {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}}

.strengths,
.weaknesses,
.recommendations,
.limitations {{
    margin-top: 25px;
}}

li {{
    margin-bottom: 12px;
}}

footer {{
    text-align: center;
    padding: 40px 20px;
    color: #666;
    font-size: 14px;
}}

.disclaimer {{
    background: #fff7df;
    border-left: 5px solid #d49b00;
    padding: 20px;
    margin-bottom: 35px;
    border-radius: 8px;
}}

@media (max-width: 700px) {{

    header h1 {{
        font-size: 27px;
    }}

    .container {{
        width: 94%;
    }}

    .website-card {{
        padding: 22px;
    }}

}}

</style>

</head>

<body>

<header>

<div class="container">

<h1>
Website Strength & Weakness Analyzer
</h1>

<p>
AI-powered preliminary website evaluation using Ollama
</p>

</div>

</header>


<main class="container">


<div class="disclaimer">

<strong>Important:</strong>

This report is an AI-based preliminary evaluation
based on information extracted from the websites.

It is not a professional website audit.

Some properties such as actual loading speed,
Core Web Vitals, true mobile responsiveness,
JavaScript behavior, visual appearance, and complete
accessibility compliance cannot be reliably determined
through basic HTML scraping.

</div>


<div class="summary">

<div class="summary-card">

<h3>🏆 Best Overall Website</h3>

<p>
{escape(best["url"])}
</p>

<div class="score">
{best["score"]}/10
</div>

</div>


<div class="summary-card">

<h3>⚠️ Lowest Overall Score</h3>

<p>
{escape(weakest["url"])}
</p>

<div class="score">
{weakest["score"]}/10
</div>

</div>

</div>


<section class="comparison">

<h2>📊 Website Comparison</h2>

<table>

<thead>

<tr>

<th>Category</th>

{headers}

</tr>

</thead>

<tbody>

{comparison_rows}

</tbody>

</table>

</section>


{website_sections}


</main>


<footer>

Website Strength & Weakness Analyzer<br>

Powered by Python + BeautifulSoup + Ollama

</footer>


</body>

</html>
"""

    return html_content


def save_report(results, comparison):
    """
    Generate and save the HTML report.
    """

    html_content = generate_report(
        results,
        comparison
    )

    with open(
        "analysis_report.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html_content)

    return "analysis_report.html"