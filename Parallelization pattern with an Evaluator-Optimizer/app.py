import asyncio
import gradio as gr

from workflow import improve_email


EXAMPLE_EMAIL = """Hi Ahmed,

You didn't send the report yesterday and we really need it ASAP.
Please send it today because we need to finish the client presentation.

Thanks.
"""


def run_workflow(email: str):
    if not email.strip():
        return (
            "Please enter an email.",
            "",
            "",
            "",
        )

    try:
        result = asyncio.run(improve_email(email))

        reviews = result["reviews"]

        reviews_text = f"""
### Grammar Review

{reviews[0]}

---

### Tone Review

{reviews[1]}

---

### Clarity Review

{reviews[2]}

---

### Business Review

{reviews[3]}
""".strip()

       
        evaluations = result["evaluations"]

        evaluation_text = ""

        for item in evaluations:
            evaluation_text += (
                f"### Iteration {item['iteration']}\n\n"
                f"{item['evaluation']}\n\n"
                "---\n\n"
            )


        final_email = result["final_email"]

        status = (
            "✅ APPROVED"
            if result["approved"]
            else "⚠️ Maximum iterations reached"
        )

        final_text = f"""
{status}

### Final Email

{final_email}

### Iterations

{result["iterations"]}
""".strip()

        return (
            reviews_text,
            result["initial_draft"],
            evaluation_text.strip(),
            final_text,
        )

    except Exception as e:
        return (
            f"Error: {e}",
            "",
            "",
            "",
        )


with gr.Blocks(title="Business Email Reviewer") as gui:

    gr.Markdown(
        """
        # 📧 Business Email Reviewer & Optimizer

        Analyze a business email from multiple perspectives,
        improve it, evaluate the result, and iteratively optimize it.
        """
    )

    email_input = gr.Textbox(
        label="Business Email",
        placeholder="Paste your email here...",
        lines=10,
        value=EXAMPLE_EMAIL,
    )

    submit_button = gr.Button(
        "Review & Improve",
        variant="primary",
    )

    with gr.Row():
        reviews_output = gr.Markdown(
            label="Parallel Reviews"
        )

        initial_output = gr.Markdown(
            label="Initial Improved Draft"
        )

    with gr.Row():
        evaluation_output = gr.Markdown(
            label="Evaluator"
        )

        final_output = gr.Markdown(
            label="Final Result"
        )

    submit_button.click(
        fn=run_workflow,
        inputs=email_input,
        outputs=[
            reviews_output,
            initial_output,
            evaluation_output,
            final_output,
        ],
    )


if __name__ == "__main__":
    gui.launch()