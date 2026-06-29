import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "poolside/laguna-m.1-20260312:free"


def get_joke(category="general"):

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"""
Generate ONE {category} joke.

Rules:
- Funny
- Family friendly
- Under 30 words
- Return ONLY the joke.
"""
            }
        ],
        "max_tokens": 100
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    print("\nTool Response:")
    print(result)

    if "error" in result:
        return "Tool Error: " + result["error"]["message"]

    if "choices" not in result:
        return "Unexpected API response."

    return result["choices"][0]["message"]["content"]