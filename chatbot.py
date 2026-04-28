import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

from matplotlib import text

print("🚀 chatbot.py is running...")

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("API KEY:", os.getenv("GROQ_API_KEY"))  # debug

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_chatbot_response(user_msg):
    
    prompt = f"""
You are a medical assistant.

Simplify the medical report and extract:

Diseases
Symptoms
Medications
Tests

Format:

Simplified Report:
...

Diseases:
...

Symptoms:
...

Medications:
...

Tests:
...

Medical Report:
{text}
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant. Explain reports in simple language."
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print("🤖 Chatbot started (type 'exit' to stop)\n")

    while True:
        user = input("You: ")
        if user.lower() == "exit":
            print("Goodbye 👋")
            break

        response = get_chatbot_response(user)
        print("Bot:", response)