 # AI Competitor Analyzer

An automated competitive analysis tool that extracts competitor website data and uses **local, open-source LLMs (via Ollama)** to generate structured market research reports — with no data ever leaving your machine.

---

## Overview

Manual competitor analysis is time-consuming and often requires sending sensitive research data to third-party AI services.

**AI Competitor Analyzer** solves this by validating competitor URLs, scraping website content, and analyzing the extracted information entirely with a **local LLM through Ollama**. Results are presented as structured competitive insights through a simple **Streamlit** interface.

---

## Key Benefits

- **Data Privacy:** All AI processing happens locally via Ollama — no data sent to external APIs.
- **Zero API Fees:** Runs on free, open-source local LLMs instead of paid AI services.
- **URL Validation:** Verifies URL syntax and site accessibility before scraping begins.
- **Robust Error Handling:** Gracefully handles connection errors, invalid responses, and failed extractions.
- **Structured Insights:** Produces organized reports on value propositions, target audiences, features, and pricing.

---

## Tech Stack

- **Language:** Python 3.9+
- **Frontend / UI:** Streamlit
- **AI Engine:** Ollama (local LLM via OpenAI SDK)
- **Web Scraping & Extraction:** Requests, BeautifulSoup4, Trafilatura
- **URL Handling & Validation:** Urllib

---

## How It Works

```
Competitor URLs
      ↓
URL Validation & Filtering
      ↓
Website Scraping
      ↓
Content Extraction
      ↓
Local LLM Analysis
      ↓
Structured Competitive Report
```

### 1. URL Validation
`urls_filter()` validates URL structure and confirms the target site is reachable before scraping begins. Malformed URLs or unsuccessful HTTP responses are automatically filtered out.

### 2. Website Scraping
`fetch_website_contents()` retrieves page HTML using **Requests**. **Trafilatura** is used first to extract the main body text; if extraction fails, **BeautifulSoup4** serves as a fallback, stripping out scripts, styles, images, navigation, and footers to isolate relevant content.

### 3. Link Extraction
`fetch_website_links()` uses **Requests** and **BeautifulSoup4** to collect all `<a>` element links from the target website.

### 4. AI Analysis
Extracted content is passed to a **local LLM running through Ollama**, which analyzes the competitor and generates a structured competitive intelligence report.

---

## Prerequisites

Before running this project, ensure you have:

1. **Python 3.9+** installed
2. **Ollama** installed and running locally on port `11434`
3. A local LLM model pulled through Ollama (e.g. `phi3` or `llama3`)

Pull a model with:

```bash
ollama pull phi3
```

---

## Installation

**1. Clone the repository**

```bash
git clone <repository-url>
cd AI-Competitor-Analyzer
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the application**

```bash
streamlit run app.py
```

---

## Output

The application generates a structured competitive analysis report covering:

- 🎯 Target Audience
- 💡 Value Proposition
- ⚙️ Key Features
- 💰 Pricing Model
- 📈 Competitive Insights

---

## Privacy

All AI analysis is performed **locally** through Ollama — extracted competitor data never leaves your machine or reaches an external AI service. The application only accesses **publicly available** content from the competitor websites you provide.

---

## Future Improvements

- Competitor comparison dashboard
- Automated competitor monitoring
- PDF report export
- Historical competitor tracking
- Support for additional local LLMs

---

## Author

**Menna Tullah Samir Mahmoud**
Computer Science & Artificial Intelligence Student
AI & Automation Enthusiast