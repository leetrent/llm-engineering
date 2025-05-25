import os
from dotenv import load_dotenv
from openai import OpenAI

# Load and verify API key
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ No API key found in .env.")

client = OpenAI(api_key=api_key)

def summarize_text(text, max_chars=2000):
    trimmed = text[:max_chars]
    prompt = f"Please summarize the following webpage text:\n\n{trimmed}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
