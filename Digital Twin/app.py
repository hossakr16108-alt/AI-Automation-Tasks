import os
import gradio as gr
from ai_engine import run_agent

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 Mennatullah Samir | AI Portfolio & Autonomous Assistant")
    gr.Markdown("Welcome to my interactive portfolio. Explore my background, projects, or chat directly with my AI digital twin powered by local LLMs.")
    
    with gr.Tabs():
        
        with gr.TabItem("💬 Chat with AI Assistant"):
            gr.Markdown("Ask anything about my skills, education, experience, or projects, and my autonomous agent will fetch the answers for you!")
            gr.ChatInterface(
                fn=run_agent,
                chatbot=gr.Chatbot(height=450),
                textbox=gr.Textbox(placeholder="Ask me anything about Mennaallah's background...", container=False, scale=7),
                title="",
                retry_btn=None,
                undo_btn=None,
                clear_btn="Clear Chat"
            )
            
        with gr.TabItem("👤 About Me & Profile"):
            with gr.Row():
                with gr.Column(scale=1):
                    if os.path.exists("profile.jpg"):
                        gr.Image("profile.jpg", label="Mennatullah Samir", elem_id="profile-img")
                    else:
                        gr.Markdown("*(Please place your 'profile.jpg' image in the project folder)*")
                    
                    gr.Markdown("### 📌 Quick Links")
                    gr.Markdown("- **Email:** mntallhmstfy668@gmail.com")
                    gr.Markdown("- **LinkedIn:** [Profile Link](https://www.linkedin.com/in/menna-tullah-samir-121a1b2b7/)")
                    gr.Markdown("- **GitHub:** [Repositories](https://github.com/mntallhmstfy668-sys)")
                    
                with gr.Column(scale=2):
                    gr.Markdown("### 🎓 Professional Bio & Background")
                    gr.Markdown("""
                    Hello! I'm **Mennatullah Samir**, a Computer Science and Artificial Intelligence undergraduate at Benha University and a graduate of Sharkya STEM School. 

                    I specialize in **AI automation, workflow engineering, and Retrieval-Augmented Generation (RAG) pipelines**. My passion lies in building intelligent systems, multi-API integrations, and deploying local LLM solutions using tools like Python, n8n, LangChain, and Ollama.

                    * **Core Focus:** Generative AI, LLM Agents, Tool-Calling, and Process Automation.
                    * **Ambition:** Bridging the gap between advanced AI models and practical, real-world automated workflows.
                    """)
                    
        with gr.TabItem("💡 Projects & Technical Stack"):
            gr.Markdown("### 🛠️ Featured Projects")
            gr.Markdown("""
            1. **AI Research Assistant (RAG & Gradio)**
               - Autonomous research agent using 6 tools (search, scrape, summarize, compare, report, RAG memory).
               - **Tech Stack:** Python, Ollama (qwen2.5:7b), Gradio, ChromaDB, LangChain.
               - **GitHub:** [Ai_Research_Assistant](https://github.com/mntallhmstfy668-sys/Ai_Research_Assistant-)

            2. **CV & Job Description Matcher**
               - Two-pass local LLM pipeline to ingest resumes/portfolios and score match percentages against job descriptions.
               - **Tech Stack:** Python, Streamlit, Ollama (Llama 3.1:8b).
               - **GitHub:** [Resume-Analyzer](https://github.com/mntallhmstfy668-sys/Resume-Analyzer)

            3. **AI-Powered STEM Student Chatbot Assistant**
               - Conversational assistant explaining complex STEM concepts using structured prompt templates.
               - **Tech Stack:** Python, Streamlit, Prompt Engineering.
               - **GitHub:** [GPT-40-ChatBot-using-Streamlit](https://github.com/mntallhmstfy668-sys/GPT-4o-ChatBot-using-Streamlit)

            4. **Fruits Classification System**
               - Supervised multi-class image classification and evaluation pipeline.
               - **Tech Stack:** Python, Scikit-learn.
               - **GitHub:** [fruit-classifier](https://github.com/mntallhmstfy668-sys/fruit-classifier)
            """)
            
            gr.Markdown("### ⚙️ Core Technical Skills")
            gr.Markdown("- **AI & Machine Learning:** NLP, Supervised Learning, Scikit-learn, PyTorch, Prompt Engineering, Text Classification.")
            gr.Markdown("- **Generative AI / LLMs:** LLM Agents & Tool-Calling, RAG, LangChain, Ollama, ChromaDB, Sentence-Transformers.")
            gr.Markdown("- **Automation:** n8n, Multi-API Workflow Automations.")
            gr.Markdown("- **Frameworks & Languages:** Python, C++, Dart, Streamlit, Gradio, Flutter.")

if __name__ == "__main__":
    demo.launch() 