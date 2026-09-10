"""
ai_engine.py
------------
Handles communication with a local LLM (served via Ollama) using the
OpenAI Python SDK's compatibility layer, to produce a structured
scientific synthesis of one or more research papers.
"""

from openai import OpenAI

# ---------------------------------------------------------------------------
# Client Configuration
# Ollama exposes an OpenAI-compatible API at /v1. No real API key is needed,
# but the SDK requires a non-empty string.
# ---------------------------------------------------------------------------
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# Change this to whichever model you have pulled locally, e.g.:
#   ollama pull llama3
#   ollama pull phi3
MODEL_NAME = "phi3"

# Generation settings
TEMPERATURE = 0.3      # Low temperature: favor factual consistency over creativity
MAX_TOKENS = 4096       # Ample room for a multi-paper synthesis; adjust to your model's context


# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are an Expert AI Research Assistant with deep expertise in machine learning, \
deep learning architectures, NLP, and computer science research methodology. \
Your job is to read raw, scraped text from multiple AI research papers, technical \
documentation pages, or articles, and produce a rigorous, well-organized scientific \
synthesis for a technically sophisticated reader (e.g., an ML engineer or researcher).

You will be given content for one or more papers, each clearly delimited with a \
header in the form "--- PAPER N ---", followed by its SOURCE URL and CONTENT.

STRICT REQUIREMENTS — YOU MUST FOLLOW ALL OF THESE:

1. ANALYZE EVERY SINGLE PAPER PROVIDED. Do not skip, omit, merge, or silently drop \
any paper, even if its scraped content is short, noisy, incomplete, or appears to be \
a failed retrieval. If a paper's content is insufficient to analyze, explicitly say so \
under that paper's section rather than omitting the paper entirely.

2. For EACH paper, produce a dedicated section with this exact structure:

   ## Paper N: <Best-guess title or domain/topic derived from the content, with source URL>

   **1. Core Problem / Objective**
   - What problem is this work trying to solve? What gap or need motivates it?

   **2. Proposed Methodology / Architecture**
   - Describe the approach, model architecture, algorithm, framework, or technique \
proposed. Be specific about novel components when they are mentioned.

   **3. Key Results & Contributions**
   - Summarize the main findings, performance numbers, benchmarks, or stated \
contributions. Note any concrete metrics if present in the text.

   **4. Limitations or Future Work**
   - Identify explicitly stated limitations, open problems, or future work. If the \
source text does not mention any, state: "Not explicitly discussed in the provided content."

3. AFTER all individual paper sections, add a final section titled:

   ## Comparative Synthesis

   In this section:
   - Identify overlaps: shared problems, techniques, datasets, or goals across papers.
   - Identify differences: contrasting approaches, assumptions, or scope.
   - Identify advancements: how later or more sophisticated papers build upon, \
improve, or diverge from ideas in the others (do not assume chronology unless the \
text indicates it — describe conceptual advancement instead).
   - If only one paper was provided, note that a comparative synthesis is limited \
to a single source and instead summarize its standalone significance in context of \
the broader field.

4. FORMATTING RULES:
   - Output STRICTLY in clean, valid Markdown.
   - Use "##" for paper/section headers and "**bold**" for the four sub-headers within \
each paper, exactly as shown above.
   - Use bullet points ("- ") for lists. Do not use tables.
   - Do NOT include any preamble, meta-commentary, apologies, or statements like \
"Here is the synthesis". Begin directly with the first paper's header.
   - Do NOT fabricate information that is not supported by the provided content. If \
information is missing or unclear, say so plainly rather than guessing confidently.
   - Be precise, technical, and concise. Avoid filler language and generic statements.

Your goal is to produce a document a researcher could use to quickly understand, \
compare, and contextualize all the provided papers without needing to read the \
original sources.
"""


def synthesize_papers(all_content: str) -> str:
    """
    Send aggregated paper content to the local LLM and return a structured
    Markdown synthesis.

    Args:
        all_content (str): Aggregated, labeled text of all scraped papers
                            (as produced by scraper.get_website_content).

    Returns:
        str: Markdown-formatted synthesis, or an error message string if the
             local model call fails (e.g., Ollama not running).
    """
    if not all_content or not all_content.strip():
        return "⚠️ No content was provided to synthesize."

    user_prompt = (
        "Analyze the following research paper content and produce the full "
        "structured synthesis as instructed:\n\n"
        f"{all_content}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        # Common cause: Ollama isn't running, or the model hasn't been pulled locally.
        return (
            "❌ **Error contacting the local LLM.**\n\n"
            f"Details: `{e}`\n\n"
            "Make sure Ollama is running (`ollama serve`) and that the model "
            f"`{MODEL_NAME}` has been pulled (`ollama pull {MODEL_NAME}`)."
        )
