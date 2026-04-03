import requests
from backend.config import OLLAMA_BASE_URL, MODEL_NAME
from backend.prompts.islamic_prompt import SYSTEM_PROMPT


def generate_answer(context, question):
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]