import requests
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama_l:11434")


def translate(text, target_lang="English"):
    prompt = f"Translate the following text to {target_lang}:\n\n{text}"

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    # ✅ Safe handling
    if "response" in data:
        return data["response"]
    else:
        print("Translator error:", data)
        return text  # fallback