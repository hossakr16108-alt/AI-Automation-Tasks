import os
import gradio as gr
from agent import chat

EXAMPLES = [
    "What did you study?",
    "Tell me about your projects",
    "What are your strongest skills?"
]

if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(
            show_label=False,
            type="messages"
        ),
        type="messages",
        theme=gr.themes.Base()
    ).launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))