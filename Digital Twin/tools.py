import os
import json
from datetime import datetime

def search_my_portfolio(query: str) -> str:
    try:
        if not os.path.exists("summary.txt"):
            return "Error: Portfolio summary file not found."
            
        with open("summary.txt", "r", encoding="utf-8") as f:
            content = f.read()
            
        return content
    except Exception as e:
        return f"Error reading portfolio file: {str(e)}"

def handle_unknown_question(user_question: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Question: {user_question}\n"
    
    try:
        with open("unknown_questions.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Error logging question: {e}")
        
    return (
        "I'm sorry, but this specific information is not currently available in my portfolio or resume. "
        "However, your question has been logged. Feel free to contact me directly through my available social or email channels!"
    )

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "search_my_portfolio",
            "description": "Use this tool to retrieve information about Mennaallah (her projects, skills, education, and background) from the summary file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific query or topic to search for in the portfolio."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_unknown_question",
            "description": "Use this tool exclusively when a visitor asks a question that cannot be answered using the portfolio summary data, in order to log the question and return a polite fallback response.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_question": {
                        "type": "string",
                        "description": "The question asked by the visitor that has no available answer in the portfolio."
                    }
                },
                "required": ["user_question"]
            }
        }
    }
]

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if callable(tool) else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results