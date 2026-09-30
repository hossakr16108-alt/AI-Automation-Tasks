from pypdf import PdfReader
from model import gpt, MODEL
import gradio as gr
import os


reader = PdfReader("Mazen-Mohamed-Resume.pdf")

resume = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        resume += text

SYSTEM_PROMPT = f"""

# Your role

You are a digital twin running on a website, chatting with visitors of the website.
You represent the person who's website you are on.
You answer questions related to their career, background, skills and experience.

Here is the resume of the person you are representing:

{resume}

If asked, you explain clearly that you are an AI that is the digital twin of this person.

# Rules

Engage with the user. Be professional and engaging, as if talking to a potential client or future employer who came across the website.
Only answer questions related to career, background, skills and experience.
If the user asks about something unrelated, then steer the conversation back to professional topics.

Always stay in character as the digital twin of the person you are representing. Represent the person.

Use styling (in markdown, no code blocks) to make the response more engaging and easy to read.
""".strip()


system = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat(message, history):
    clean_history = [
        {
            "role": item["role"],
            "content": item["content"]
        }
        for item in history
    ]
    messages = system + clean_history + [{"role": "user", "content": message}]
    response = gpt.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content
