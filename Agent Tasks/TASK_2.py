import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import gradio as gr

local_client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1/",
)

model = OpenAIChatCompletionsModel(
    model="llama3",
    openai_client=local_client,
)

sentiment_worker = Agent(
    name="SentimentWorker",
    instructions="Analyze the sentiment of the customer review (Positive, Negative, or Neutral).",
    model=model,
)

response_worker = Agent(
    name="ResponseWorker",
    instructions="Draft a polite and professional customer service response.",
    model=model,
)

sentiment_tool = sentiment_worker.as_tool(
    tool_name="sentiment_analysis_tool",
    description="Use this tool to analyze the sentiment of a customer review."
)

response_tool = response_worker.as_tool(
    tool_name="response_writer_tool",
    description="Use this tool to draft a professional response based on the customer issue."
)

orchestrator_agent = Agent(
    name="OrchestratorAgent",
    instructions="You are a customer service supervisor. Use the provided tools to analyze the review and draft a response, then coordinate them.",
    model=model,
    tools=[sentiment_tool, response_tool]
)

evaluator_optimizer_agent = Agent(
    name="EvaluatorOptimizer",
    instructions="Review the orchestrator's output. Evaluate its tone, accuracy, and professionalism, then optimize and format it into a final polished customer support report.",
    model=model,
)

async def process_orchestrator_task(customer_review: str) -> str:
    if not customer_review.strip():
        return "Please enter a valid customer review."

    orchestrator_prompt = f"Process this customer review and use the tools: {customer_review}"
    orchestrator_result = await Runner.run(orchestrator_agent, orchestrator_prompt)
    
    optimization_prompt = f"Evaluate and optimize the following output into a final professional report:\n{orchestrator_result.final_output}"
    final_result = await Runner.run(evaluator_optimizer_agent, optimization_prompt)
    
    return final_result.final_output

def run_gradio_app(review_text):
    return asyncio.run(process_orchestrator_task(review_text))

demo = gr.Interface(
    fn=run_gradio_app,
    inputs=gr.Textbox(lines=4, label="Customer Review", placeholder="Type the customer review here..."),
    outputs=gr.Textbox(lines=10, label="Final Optimized Response"),
    title="AI Customer Support (Orchestrator-Workers via .as_tool + Evaluator-Optimizer)",
    description="Local execution using Ollama and Gradio."
)

if __name__ == "__main__":
    demo.launch()