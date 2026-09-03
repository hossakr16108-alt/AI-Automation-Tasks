# 🤖 AI Resume & Portfolio Job Matcher

An AI-powered pipeline built with **Streamlit** and **Ollama** (`llama3.1:8b`) that automates candidate profiling and resume-to-job matching. The system accepts raw text, PDF/DOCX resumes, or portfolio URLs, extracts structured JSON profile data, and generates a comparative match report against job descriptions — all running **100% locally**.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-Input Ingestion** | Supports raw text, PDF/DOCX file uploads, and live portfolio web scraping |
| **Structured Extraction (Pass 1)** | Converts unstructured candidate text into a validated JSON schema |
| **Match Report Generation (Pass 2)** | Produces match scores, key strengths, missing skill gaps, and hiring recommendations |
| **100% Local Inference** | Runs entirely via Ollama — full data privacy, zero external API costs |

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit
- **LLM Engine:** Ollama (`llama3.1:8b` via OpenAI-compatible Python SDK)
- **Web Scraping:** BeautifulSoup4, Requests
- **File Parsing:** `pypdf`, `python-docx`

---

## 📂 Project Structure

```
├── app.py                  # Main Streamlit UI application
├── ai_engine.py             # Ollama API client & prompt definitions
├── scraper.py               # Web scraping & PDF/DOCX text extraction utilities
├── requirements.txt         # Python dependency list
└── README.md                # Project documentation
```

---

## 🧠 How It Works

```
                 ┌─────────────────────┐
   Input ──────► │  Ingestion Layer     │  (raw text / PDF / DOCX / URL)
                 │  (scraper.py)        │
                 └──────────┬───────────┘
                            │  cleaned text
                            ▼
                 ┌─────────────────────┐
                 │  Pass 1: Profile     │  → structured JSON
                 │  Extraction (LLM)    │
                 └──────────┬───────────┘
                            │  candidate profile JSON
                            ▼
                 ┌─────────────────────┐
                 │  Pass 2: Job Match   │  → match score, strengths,
                 │  Analysis (LLM)      │     gaps, recommendation
                 └──────────┬───────────┘
                            ▼
                     Streamlit Report UI
```

1. **Ingest** — the candidate's resume or portfolio is normalized into plain text.
2. **Extract** — the LLM parses that text into a structured JSON profile (skills, experience, education, etc.).
3. **Match** — the profile JSON is compared against a target job description to produce a scored, explainable report.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running

### 2. Pull and Verify the Local Model

```bash
ollama pull llama3.1:8b
ollama run llama3.1:8b "hi"
```

### 3. Clone the Repository & Install Dependencies

```bash
git clone https://github.com/your-username/resume-portfolio-matcher.git
cd resume-portfolio-matcher

python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

`requirements.txt`:
```
streamlit
openai
ollama
beautifulsoup4
requests
pypdf
python-docx
```

### 4. Run the App

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📝 Usage

1. Launch the app and choose an input method: **Raw Text**, **Upload PDF/DOCX**, or **Portfolio URL**.
2. Click **Extract Profile** to run Pass 1 — review the generated JSON candidate profile.
3. Paste or upload the target **job description**.
4. Click **Generate Match Report** to run Pass 2 — view the match score, strengths, gaps, and recommendation.
5. Optionally export the report (e.g. copy as Markdown/JSON) for sharing.

---

## ⚡ Performance Optimization Tips

If running inference on a local CPU:

1. **Truncate input** — text inputs are automatically capped at ~3,000 characters to prevent high latency.
2. **Limit crawl depth** — portfolio link extraction is capped at 2 links max.
3. **Use a lighter model** — swap in `qwen2.5:7b` or `phi3:mini` for faster response times:
   ```bash
   ollama pull phi3:mini
   ```
   then update the model name in `ai_engine.py`.
4. **Reuse a warm model** — keep `ollama run <model>` active in a background terminal to avoid cold-start delays between requests.

---

## 🩺 Troubleshooting

| Issue | Likely Cause / Fix |
|---|---|
| `Connection refused` to Ollama | Ollama isn't running — start it with `ollama serve` |
| Very slow first response | Cold model load — first inference call always warms up the model |
| Empty/malformed JSON from Pass 1 | Input text too noisy — check `scraper.py` output before sending to the LLM |
| Scraper returns no text | Site may be JS-rendered; BeautifulSoup only parses static HTML |

---

## 🗺️ Roadmap

- [ ] Batch matching (one resume vs. multiple job descriptions)
- [ ] Exportable PDF/Word match reports
- [ ] Support for additional local model backends (LM Studio, vLLM)
- [ ] Confidence scoring for extracted JSON fields

---

## 🤝 Contributing

Contributions are welcome! Please open an issue to discuss significant changes before submitting a pull request.

## 📄 License

This project is licensed under the MIT License — see the `LICENSE` file for details.
