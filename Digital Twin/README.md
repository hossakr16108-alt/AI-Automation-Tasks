# 🚀 Digital Twin | AI Portfolio & Autonomous Assistant

An interactive portfolio for **Mennatullah Samir Mahmoud** with an AI "digital twin" that answers visitors' questions about her background, skills, education, and projects. It runs **100% locally** using Ollama and qwen2.5, so no data leaves the machine and there are no API costs.

## ✨ Features

- **💬 AI chat assistant:** an autonomous agent that uses tool-calling to look up portfolio data before answering, and never makes up facts.
- **👤 About Me & Profile:** photo, quick links, and a professional summary generated from the CV.
- **💡 Projects & Technical Stack:** featured projects with tech stacks and GitHub links.
- **❓ Unknown-question handling:** questions outside the portfolio are logged and answered with a polite fallback.

## 🧠 How It Works

```
linkedin.pdf ──► context.py ──► summary.txt ──► tools (search_my_portfolio)
                                      │                     │
                                      ▼                     ▼
                                  app.py  ◄──────────  ai_engine.py (qwen2.5 via Ollama)
                              (Gradio interface)
```

1. `context.py` extracts the text from `linkedin.pdf` into `summary.txt`.
2. `ai_engine.py` sends the visitor's message to the local model, which decides which tool to call.
3. `tools.py` defines the tools the agent can use (`search_my_portfolio`, `handle_unknown_question`).
4. `app.py` serves everything through a Gradio web interface.

## 📁 Project Structure

```
Digital_Twin/
├── app.py           # Gradio UI (chat, profile, projects tabs)
├── ai_engine.py     # Agent loop: model calls + tool-calling
├── tools.py         # Tool definitions and handlers
├── context.py       # Extracts linkedin.pdf → summary.txt
├── linkedin.pdf     # Source knowledge base (must contain a real text layer)
├── summary.txt      # Generated text used by the app and the agent
└── profile.jpg      # Profile photo shown in the About tab
```

## ⚙️ Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running
- Python packages: `gradio`, `openai`, `pypdf`

## 🛠️ Setup

**1. Install Ollama and pull the model**

```bash
ollama pull qwen2.5
```

**2. Install the Python dependencies**

```bash
pip install gradio openai pypdf
```

**3. Prepare the knowledge base**

Place `linkedin.pdf` and `profile.jpg` in the project folder, then generate `summary.txt`:

```bash
python context.py
```

You should see a message like `✅ Success: Extracted 4 pages (... chars)`. Open `summary.txt` and make sure the text is readable before continuing.

**4. Run the app**

```bash
python app.py
```

Then open http://127.0.0.1:7860 in your browser.

## 🔧 Configuration

`ai_engine.py` reads its settings from environment variables, with these defaults:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama's OpenAI-compatible endpoint |
| `OLLAMA_API_KEY` | `ollama` | Placeholder key (Ollama ignores it) |
| `PORTFOLIO_MODEL` | `llama3.1` | Model used by the agent |

## 🩺 Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `summary.txt` is empty | The PDF has no real text layer (text drawn as vector outlines or images). Export a new PDF from a text-based tool such as Word, or the browser's **Print → Save as PDF**, then rerun `context.py`. |
| About tab still shows old or empty text | `app.py` reads `summary.txt` only at startup. Stop it and run `python app.py` again after regenerating the file. |
| "Couldn't reach the local model server" | Ollama isn't running. Start it and confirm the model is pulled with `ollama list`. |
| Profile photo missing | Make sure `profile.jpg` is in the same folder as `app.py`. |

## 👩‍💻 Author

**Mennatullah Samir Mahmoud** — Computer Science & AI student at Benha University

- 📧 mntallhmstfy668@gmail.com
- 💼 [LinkedIn](https://www.linkedin.com/in/menna-tullah-samir-121a1b2b7/)
- 🐙 [GitHub](https://github.com/mntallhmstfy668-sys)
