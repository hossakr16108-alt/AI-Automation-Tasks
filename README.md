# 🦙 Website Strength & Weakness Analyzer

An AI-powered Python application that analyzes and compares three websites using **Ollama**, a locally running Large Language Model (LLM).

The application fetches website content, extracts useful information using **BeautifulSoup**, sends the cleaned information to a local Ollama model, and generates an AI-based evaluation of each website's strengths, weaknesses, scores, and recommendations.

---

## 📌 Project Overview

The **Website Strength & Weakness Analyzer** allows a user to enter three website URLs and receive a structured comparison.

The system analyzes:

* User Experience
* Content Quality
* Navigation
* SEO indicators
* Accessibility indicators
* Trust and credibility indicators
* Overall website quality
* Strengths
* Weaknesses
* Recommendations

The final results can be viewed in the terminal, saved as JSON, and generated as an HTML report.

> **Important:** This project provides an AI-based preliminary evaluation. It is not a replacement for professional SEO, accessibility, performance, or security auditing tools.

---

## 🎯 Objectives

The main objectives of this project are:

1. Accept three website URLs from the user.
2. Fetch website HTML using Python.
3. Extract useful website information using BeautifulSoup.
4. Clean and limit the extracted content.
5. Send the information to a locally running Ollama LLM.
6. Analyze the strengths and weaknesses of each website.
7. Generate scores for different website categories.
8. Compare the three websites.
9. Generate a readable final report.

---

## 🏗️ System Architecture

```text
User
 │
 │ Enter 3 URLs
 ▼
Python Application
 │
 ▼
Requests
 │
 │ Fetch HTML
 ▼
Website HTML
 │
 ▼
BeautifulSoup
 │
 │ Extract & Clean
 ▼
Website Information
 │
 ▼
Ollama
 │
 │ Local LLM Analysis
 ▼
AI Evaluation
 │
 ├── Strengths
 ├── Weaknesses
 ├── Scores
 └── Recommendations
 │
 ▼
Website Comparison
 │
 ├── Terminal Results
 ├── JSON Results
 └── HTML Report
```

---

## 🛠️ Technologies Used

### Python

The main programming language used to build the application.

Python handles:

* User input
* Website requests
* Data processing
* AI communication
* Report generation
* Error handling

### Requests

The `requests` library is used to retrieve HTML content from websites.

### BeautifulSoup4

BeautifulSoup is used to parse HTML and extract:

* Page title
* Headings
* Visible text
* Links
* Meta description
* Basic page structure

### Ollama

Ollama allows the project to run a Large Language Model locally.

The website information is sent to Ollama, which evaluates the website and produces:

* Strengths
* Weaknesses
* Scores
* Recommendations
* Comparisons

No OpenAI API key or paid AI API is required.

---

## 📁 Project Structure

```text
website-analyzer/
│
├── main.py
├── website_scraper.py
├── ollama_analyzer.py
├── prompts.py
├── report_generator.py
├── test_ollama.py
├── requirements.txt
├── .gitignore
│
└── tests/
    ├── README.md
    └── test_scraper.py
```

### `main.py`

The main entry point of the application.

It:

* Gets the three URLs
* Runs the scraper
* Sends information for AI analysis
* Displays results
* Compares websites
* Saves JSON results
* Generates the HTML report

### `website_scraper.py`

Responsible for retrieving and processing website HTML.

### `ollama_analyzer.py`

Handles communication with the local Ollama model and processes the AI response.

### `prompts.py`

Contains the prompts used to instruct Ollama how to analyze the websites.

### `report_generator.py`

Creates the final HTML report.

### `test_ollama.py`

Tests whether Python can communicate successfully with Ollama.

### `tests/`

Contains basic project tests.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mariamezayed2006-eng/website-strength-weakness-analyzer.git
```

Then enter the project folder:

```bash
cd website-strength-weakness-analyzer
```

---

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

## 🦙 Ollama Setup

Install Ollama on your computer.

After installation, check that it is available:

```powershell
ollama --version
```

Start Ollama and download a model.

For example:

```powershell
ollama pull llama3.2
```

Check the installed models:

```powershell
ollama list
```

Test the model:

```powershell
ollama run llama3.2
```

---

## ▶️ Running the Project

Make sure the virtual environment is active:

```powershell
.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python main.py
```

The program will ask for three website URLs.

Example:

```text
========================================
WEBSITE STRENGTH & WEAKNESS ANALYZER
========================================

Enter Website 1 URL:
https://www.apple.com

Enter Website 2 URL:
https://www.wikipedia.org

Enter Website 3 URL:
https://www.python.org
```

The application will then scrape and analyze the websites.

---

## 📊 Evaluation Categories

Each website receives an AI-generated score from **1–10** for:

| Category          | Description                                                            |
| ----------------- | ---------------------------------------------------------------------- |
| User Experience   | How clear and user-friendly the available content and structure appear |
| Content Quality   | Organization, usefulness, and clarity of content                       |
| Navigation        | Quality and organization of available navigation elements              |
| SEO               | Detectable SEO-related indicators such as title and metadata           |
| Accessibility     | Detectable accessibility indicators such as image alt text             |
| Trust/Credibility | Detectable trust signals and credibility-related information           |
| Overall           | Combined evaluation of the available categories                        |

The scores are intended as a **preliminary AI evaluation**, not objective professional measurements.

---

## 🔎 What the Analyzer Can Detect

The scraper can collect information such as:

* Page title
* Headings
* Visible text
* Links
* Meta description
* Basic HTML structure
* Images and available accessibility attributes
* Other detectable HTML information

The AI uses this information to identify potential strengths, weaknesses, and recommendations.

---

## ⚠️ Limitations

The project does not perform a complete professional website audit.

Some information cannot reliably be determined through basic HTML scraping.

For example:

* Actual page loading speed
* Core Web Vitals
* Real mobile responsiveness
* JavaScript behavior
* Complete accessibility compliance
* Real user behavior
* Server performance
* Security vulnerabilities
* Detailed visual design
* Browser-specific behavior

Dynamic websites may also provide limited information because some content is generated using JavaScript after the initial HTML page loads.

The AI may also make incorrect interpretations, so its conclusions should be treated as recommendations rather than guaranteed facts.

---

## 🛡️ Responsible Analysis

The project is designed for educational and analytical purposes.

It should only be used to analyze websites in an appropriate and responsible manner.

The scraper uses normal HTTP requests and does not attempt to bypass authentication, security mechanisms, or access restrictions.

---

## 🚀 Future Improvements

Possible future versions could include:

* GUI interface
* Web application interface
* Analysis of more than three websites
* Lighthouse integration
* Real performance measurements
* Advanced accessibility testing
* More detailed SEO analysis
* Database storage
* PDF reports
* Charts and visualizations
* Website screenshots
* Multi-model Ollama comparison
* Historical website analysis
* Automated report generation

---

## 🎓 Educational Purpose

This project demonstrates how several technologies can work together:

```text
Web Scraping
      +
HTML Parsing
      +
Data Cleaning
      +
Local LLM
      +
Prompt Engineering
      +
Data Analysis
      +
Report Generation
```

It was developed as a student project to explore the practical use of **Local Large Language Models with Python applications**.

---

## 👩‍💻 Author

**Mariam**

Computer Science Student

---

## 📄 License

This project is intended primarily for educational purposes.
