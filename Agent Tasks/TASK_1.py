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

sentiment_agent = Agent(
    name="SentimentAnalyst",
    instructions="Analyze the customer review and determine the sentiment (Positive, Negative, Neutral) with a brief reason.",
    model=model,
)

issue_agent = Agent(
    name="IssueExtractor",
    instructions="Extract the core product or service issue mentioned in the customer review (e.g., shipping delay, bad quality, pricing).",
    model=model,
)

evaluator_optimizer_agent = Agent(
    name="EvaluatorOptimizer",
    instructions="""You are a Quality Assurance Manager. 
    Review the combined analysis (sentiment and issue). 
    Evaluate if it's professional and accurate, then optimize and format it into a clean, professional executive summary report for management.""",
    model=model,
)

async def process_customer_review(customer_review: str) -> str:
    if not customer_review.strip():
        return "Please enter a valid customer review."

    sentiment_task = Runner.run(sentiment_agent, customer_review)
    issue_task = Runner.run(issue_agent, customer_review)
    
    sentiment_result, issue_result = await asyncio.gather(sentiment_task, issue_task)
    
    combined_data = f"""
    Sentiment Analysis Result:
    {sentiment_result.final_output}
    
    Extracted Issue Result:
    {issue_result.final_output}
    """
    
    optimization_prompt = f"Please evaluate and optimize the following analysis into a formal management report:\n{combined_data}"
    final_result = await Runner.run(evaluator_optimizer_agent, optimization_prompt)
    
    return final_result.final_output

def run_gradio_app(review_text):
    return asyncio.run(process_customer_review(review_text))

demo = gr.Interface(
    fn=run_gradio_app,
    inputs=gr.Textbox(lines=4, label="Customer Review", placeholder="Type the customer review here..."),
    outputs=gr.Textbox(lines=10, label="Final Optimized Management Report"),
    title="AI Customer Review Analyzer (Parallel + Evaluator-Optimizer)",
    description="Enter a customer review to analyze its sentiment, extract core issues, and generate an optimized management report locally using Ollama."
)

if __name__ == "__main__":
    demo.launch()