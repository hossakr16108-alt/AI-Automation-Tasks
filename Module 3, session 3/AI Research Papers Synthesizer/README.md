# 🔬 AI Research Papers Synthesizer

An automated research paper analysis and synthesis tool. It extracts technical documentation and scientific papers directly from URLs and leverages local open-source LLMs (via Ollama) to produce structured comparative summaries — **ensuring zero API fees and 100% data privacy**.

---

## 🚀 Key Features

* **Complete Data Privacy:** All AI analysis is performed locally using Ollama; no proprietary research or reading data is sent to third-party APIs.
* **Zero Cost:** Runs locally using open-source models (such as `phi3` or `llama3`).
* **Robust Content Extraction:** Uses `Trafilatura` for primary text extraction with an automated `BeautifulSoup` fallback that strips boilerplate navigation, scripts, and styling.
* **Smart URL Validation:** Validates URL syntax and reachability via HTTP pre-checks.
* **Comparative Scientific Synthesis:** Generates a structured breakdown (Objective, Architecture, Results, Limitations) alongside a side-by-side comparative analysis.

---

## 🛠️ Architecture Pipeline

```text
Research Paper URLs
       │
       ▼
URL Validation & Reachability Check (`urlparse` + `requests`)
       │
       ▼
Content Extraction (`Trafilatura` with `BeautifulSoup` fallback)
       │
       ▼
Local LLM Prompt Chaining (`Ollama` via OpenAI Python SDK)
       │
       ▼
Structured Markdown Synthesis (Streamlit Dashboard)