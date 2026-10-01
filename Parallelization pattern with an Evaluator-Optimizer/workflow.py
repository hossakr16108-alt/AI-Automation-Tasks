import asyncio

from agents import Runner
from email_agents import (
    grammar_agent,
    tone_agent,
    clarity_agent,
    business_agent,
    generator_agent,
    evaluator_agent,
    optimizer_agent,
)


async def run_parallel_reviews(email):
    results = await asyncio.gather(
        Runner.run(grammar_agent, email),
        Runner.run(tone_agent, email),
        Runner.run(clarity_agent, email),
        Runner.run(business_agent, email),
    )

    return [result.final_output for result in results]


async def generate_initial_draft(original_email, reviews):

    prompt = f"""
Original Email:
----------------
{original_email}

Grammar Review:
----------------
{reviews[0]}

Tone Review:
----------------
{reviews[1]}

Clarity Review:
----------------
{reviews[2]}

Business Review:
----------------
{reviews[3]}

Using the reviews above, create an improved version of
the original email.
"""

    result = await Runner.run(generator_agent, prompt)

    return result.final_output


async def evaluate_and_optimize(original_email, draft, max_iterations = 3):
    current_draft = draft
    evaluations = []

    for iteration in range(1, max_iterations + 1):

        evaluation_prompt = f"""
Original Email:
----------------
{original_email}

Current Draft:
----------------
{current_draft}

Evaluate the current draft according to your criteria.
"""

        evaluation_result = await Runner.run(evaluator_agent, evaluation_prompt)

        evaluation = evaluation_result.final_output

        evaluations.append({
            "iteration": iteration,
            "evaluation": evaluation,
        })

        if evaluation.strip().upper().startswith("APPROVED"):

            return {
                "final_email": current_draft,
                "approved": True,
                "iterations": iteration,
                "evaluations": evaluations,
            }


        optimizer_prompt = f"""
Original Email:
----------------
{original_email}

Current Draft:
----------------
{current_draft}

Evaluator Feedback:
----------------
{evaluation}

Improve the current draft according to the evaluator feedback.
"""

        optimizer_result = await Runner.run(optimizer_agent,optimizer_prompt)

        current_draft = optimizer_result.final_output


    return {
        "final_email": current_draft,
        "approved": False,
        "iterations": max_iterations,
        "evaluations": evaluations,
    }


async def improve_email(email):
    
    reviews = await run_parallel_reviews(email)

    draft = await generate_initial_draft(original_email=email, reviews=reviews)

    result = await evaluate_and_optimize(original_email=email, draft=draft, max_iterations=3)

    return {
        "reviews": reviews,
        "initial_draft": draft,
        **result,
    }