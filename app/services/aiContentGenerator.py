import openai
import os
import json
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

def slugify(text: str) -> str:
    """Converts text into a Git-friendly branch slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_pr_and_tests(card_title: str, card_desc: str) -> dict:
    prompt = f"""
You're a senior software engineer. A Trello card has been created with the following information:

Title: "{card_title}"
Description: "{card_desc}"

Your tasks:
1. Generate a meaningful and professional pull request title.
2. Write a clear and helpful pull request description.
3. Generate 3–5 acceptance test cases in Markdown list format.
4. Propose a Git branch name based on the card title (kebab-case, prefix with `feature/`). Limit to 3 words in the kebab case

Respond in JSON format like:
{{
  "pr_title": "...",
  "pr_body": "...",
  "acceptance_tests": ["...", "..."],
  "branch_name": "feature/my-branch-name"
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    try:
        content = response['choices'][0]['message']['content']
        data = json.loads(content) if content.strip().startswith('{') else eval(content)
        # Fallback if branch name is missing
        if 'branch_name' not in data:
            data['branch_name'] = f"feature/{slugify(card_title)}"
        return data
    except Exception as e:
        raise RuntimeError(f"OpenAI response parsing failed: {e}")
