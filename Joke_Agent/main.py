import os
import requests

from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT
from memory import load_memory, save_memory

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found.")

MODEL = "openai/gpt-oss-20b:free"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_llm(messages):
    """
    Sends the conversation to OpenRouter and
    returns the model response.
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def agent_loop(user_input):
    """
    Main agent function.

    Loads memory
    Adds system prompt
    Adds user message
    Calls LLM
    Saves memory
    Returns final response
    """

    # Load previous conversation
    memory = load_memory()

    # Conversation
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous messages
    messages.extend(memory)

    # Add current user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Call the LLM
    result = call_llm(messages)

    assistant_message = result["choices"][0]["message"]

    # Save assistant response
    messages.append(assistant_message)

    # Save conversation (excluding system prompt)
    save_memory(messages[1:])

    # Return response text
    return assistant_message.get(
        "content",
        "No response generated."
    )


# This part runs ONLY if you execute:
# python main.py
# Streamlit ignores this block.

if __name__ == "__main__":

    print("😂 Joke Agent")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        try:
            answer = agent_loop(user_input)
            print("Agent:", answer)

        except Exception as e:
            print("Error:", e)