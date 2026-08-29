def create_website_analysis_prompt(website_data):
    """
    Create a structured JSON prompt for Ollama to analyze a website.
    """

    headings = "\n".join(
        f"- {heading}"
        for heading in website_data["headings"]
    )

    links = "\n".join(
        f"- {link['text']} -> {link['url']}"
        for link in website_data["links"][:30]
    )

    structure = website_data["basic_structure"]

    prompt = f"""
You are a website strength and weakness analysis assistant.

Your task is to perform a preliminary evaluation of a website
using ONLY the information provided below.

==================================================
IMPORTANT ANALYSIS RULES
==================================================

1. Do NOT invent facts.

2. Do NOT assume something exists if it is not shown in the
   provided website data.

3. Clearly distinguish between:
   - Observed facts
   - Reasonable inferences
   - Things that cannot be determined

4. If something cannot be reliably determined from the
   available data, say:
   "Cannot be determined from the available data."

5. Do NOT claim that you tested something that was not actually
   tested.

6. HTML scraping cannot reliably measure:
   - Actual loading speed
   - Core Web Vitals
   - Real mobile responsiveness
   - JavaScript functionality
   - Visual design quality
   - Complete accessibility compliance
   - Server performance

7. This is an AI-based preliminary evaluation, NOT a professional
   website audit.

8. Do not give a high score simply because the website is famous,
   familiar, or belongs to a well-known organization.

9. Base scores only on evidence available in the scraped data.

==================================================
SCORING SYSTEM
==================================================

Give scores from 1 to 10.

Use this scale:

1-2  = Very Poor
3-4  = Poor
5-6  = Average
7-8  = Good
9    = Very Good
10   = Excellent

The categories are:

- User Experience
- Content Quality
- Navigation
- SEO
- Accessibility
- Trust/Credibility

Scoring must be evidence-based.

If there is insufficient evidence, use a conservative score
and explain the limitation.

==================================================
WEBSITE INFORMATION
==================================================

URL:
{website_data["url"]}

PAGE TITLE:
{website_data["title"]}

META DESCRIPTION:
{website_data["meta_description"]}

==================================================
HEADINGS
==================================================

{headings if headings else "No headings were detected."}

==================================================
BASIC HTML STRUCTURE
==================================================

Language:
{structure["language"]}

Number of images:
{structure["number_of_images"]}

Images with alt text:
{structure["images_with_alt_text"]}

Number of headings:
{structure["number_of_headings"]}

Number of links:
{structure["number_of_links"]}

==================================================
LINKS
==================================================

{links if links else "No links were detected."}

==================================================
VISIBLE WEBSITE TEXT
==================================================

{website_data["visible_text"]}

==================================================
ANALYSIS TASK
==================================================

Analyze the website using the available information.

--------------------------------------------------
1. WEBSITE OVERVIEW
--------------------------------------------------

Provide:

- Website name/title
- Main purpose
- Likely target audience
- Main services, products, or content

Clearly distinguish observations from inferences.

--------------------------------------------------
2. STRENGTHS
--------------------------------------------------

Identify the website's strengths.

Consider:

- Clear purpose
- Content organization
- Navigation
- Content quality
- SEO indicators
- Accessibility indicators
- Calls to action
- Trust signals
- Information structure

For every strength, provide evidence from the website data.

--------------------------------------------------
3. WEAKNESSES
--------------------------------------------------

Identify weaknesses.

Consider:

- Missing metadata
- Poor content structure
- Navigation problems
- Missing information
- Weak calls to action
- SEO issues
- Accessibility issues
- Content organization
- Missing headings
- Missing alt text
- Weak trust indicators

For every weakness, provide evidence.

--------------------------------------------------
4. SCORES
--------------------------------------------------

Give an integer score from 1 to 10 for:

- User Experience
- Content Quality
- Navigation
- SEO
- Accessibility
- Trust/Credibility

Do NOT calculate the overall score.

Python will calculate the overall score separately.

--------------------------------------------------
5. CANNOT BE DETERMINED
--------------------------------------------------

List important things that cannot reliably be determined
from the scraped information.

Examples:

- Actual page loading speed
- Core Web Vitals
- True mobile responsiveness
- JavaScript behavior
- Complete accessibility compliance
- Visual appearance
- Server performance
- Real user behavior

--------------------------------------------------
6. RECOMMENDATIONS
--------------------------------------------------

Give 3 to 5 practical recommendations.

Recommendations should be directly related to weaknesses
identified from the available website information.

Do not recommend fixing something unless there is evidence
or a reasonable basis for the recommendation.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT put the JSON inside a ```json code block.

Use EXACTLY this structure:

{{
    "website_overview": {{
        "name": "string",
        "purpose": "string",
        "target_audience": "string",
        "main_content": "string"
    }},

    "strengths": [
        {{
            "point": "string",
            "evidence": "string"
        }}
    ],

    "weaknesses": [
        {{
            "point": "string",
            "evidence": "string"
        }}
    ],

    "scores": {{
        "user_experience": 0,
        "content_quality": 0,
        "navigation": 0,
        "seo": 0,
        "accessibility": 0,
        "trust": 0
    }},

    "cannot_be_determined": [
        "string"
    ],

    "recommendations": [
        "string"
    ]
}}

==================================================
FINAL RULES
==================================================

Return ONLY the JSON object.

The scores must be integers between 1 and 10.

Do not calculate the overall score.

Do not invent information.

Base every conclusion on the supplied website data.

If something cannot be determined, clearly state that
it cannot be determined from the available data.
"""

    return prompt


if __name__ == "__main__":

    from website_scraper import scrape_website

    website = scrape_website(
        "https://example.com"
    )

    prompt = create_website_analysis_prompt(
        website
    )

    print("=" * 60)
    print("GENERATED JSON ANALYSIS PROMPT")
    print("=" * 60)

    print(prompt)

    print("=" * 60)
    print("PROMPT GENERATION SUCCESSFUL!")
    print("=" * 60)