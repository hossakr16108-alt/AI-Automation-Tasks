"""
app.py
------
Streamlit front-end for the AI Research Papers Synthesizer.

Flow:
    1. User pastes one URL per line into a text area.
    2. On button click, URLs are parsed and validated (urls_filter).
    3. Valid URLs are scraped and aggregated (get_website_content).
    4. Aggregated content is sent to the local LLM (synthesize_papers).
    5. Result is rendered as Markdown.
"""

import streamlit as st

from scraper import urls_filter, get_website_content
from ai_engine import synthesize_papers

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Research Papers Synthesizer",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 AI Research Papers Synthesizer")
st.caption(
    "Paste links to AI research papers, technical docs, or articles below. "
    "This tool scrapes their content and uses a local LLM (via Ollama) to "
    "generate a structured, comparative scientific synthesis."
)

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
url_input = st.text_area(
    "Paper / Article URLs (one per line)",
    height=180,
    placeholder=(
        "https://arxiv.org/abs/1706.03762\n"
        "https://arxiv.org/abs/2005.14165\n"
        "https://example.com/technical-blog-post"
    ),
    help="Enter one full URL per line, including http:// or https://",
)

analyze_clicked = st.button("Analyze Papers", type="primary")

# ---------------------------------------------------------------------------
# Main Logic
# ---------------------------------------------------------------------------
if analyze_clicked:
    # --- Guard: empty input ---
    if not url_input or not url_input.strip():
        st.error("⚠️ Please paste at least one URL before analyzing.")
    else:
        # Split textarea into a clean list of candidate URLs
        raw_urls = [line.strip() for line in url_input.splitlines() if line.strip()]

        if not raw_urls:
            st.error("⚠️ No valid URL lines detected. Please check your input.")
        else:
            with st.spinner("Validating URLs..."):
                valid_urls = urls_filter(raw_urls)

            # --- Guard: no valid/reachable URLs ---
            if not valid_urls:
                st.error(
                    "❌ None of the provided URLs were valid or reachable. "
                    "Please check the links and try again."
                )
            else:
                # Inform the user which URLs were dropped, if any
                invalid_count = len(raw_urls) - len(valid_urls)
                if invalid_count > 0:
                    st.warning(
                        f"⚠️ {invalid_count} URL(s) were skipped (invalid syntax "
                        f"or unreachable). Proceeding with {len(valid_urls)} valid URL(s)."
                    )

                with st.spinner("Synthesizing research..."):
                    # Step 1: Scrape all valid papers into one aggregated string
                    all_content = get_website_content(valid_urls)

                    if not all_content or not all_content.strip():
                        st.error(
                            "❌ Content could not be extracted from any of the "
                            "provided URLs."
                        )
                    else:
                        # Step 2: Send aggregated content to the local LLM
                        synthesis_result = synthesize_papers(all_content)

                        # --- Render Result ---
                        st.success(f"✅ Synthesis complete for {len(valid_urls)} paper(s).")
                        st.markdown("---")
                        st.markdown(synthesis_result)

                        # Optional: let users inspect raw scraped content
                        with st.expander("🔍 View raw scraped content used for synthesis"):
                            st.text(all_content)
