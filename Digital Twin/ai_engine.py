import json
from openai import OpenAI
from tools import handle_tool_calls, tools_definition

DEFAULT_MODEL = "qwen2.5:3b"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def run_agent(user_message, history=None):
    if history is None:
        history = []
        
    messages = [
        {
            "role": "system",
            "content": """You are Mennaallah's official AI Portfolio Assistant, an autonomous professional representative of an AI Automation Engineer and Computer Science student.

Your core objectives:
1. Answer questions strictly based on Mennaallah's portfolio data retrieved via the 'search_my_portfolio' tool.
2. If a visitor asks about projects, skills, education, experience, or contact channels, ALWAYS use 'search_my_portfolio' first to fetch accurate details.
3. If a visitor's question cannot be answered using the portfolio data (e.g., completely unrelated topics, personal opinions, or missing data), you MUST invoke the 'handle_unknown_question' tool to log the question and output a polite fallback response.
4. Maintain a professional, welcoming, and sharp tone reflecting a top-tier tech profile. Never make up facts."""
        }
    ]
    
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
        
    messages.append({"role": "user", "content": user_message})
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        tools=tools_definition,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    
    while response_message.tool_calls:
        messages.append(response_message)
        tool_results = handle_tool_calls(response_message.tool_calls)
        messages.extend(tool_results)
        
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=tools_definition,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        
    return response_message.content