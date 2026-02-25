import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"

def analyze_medical_report(text):

    prompt = f"""
You are a medical assistant.

Return output EXACTLY in this format:

PATIENT_VIEW:
(simple explanation)

DOCTOR_VIEW:
(technical explanation)

ENTITIES:
Diseases: ...
Symptoms: ...
Medicines: ...
Tests: ...

Medical Report:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
