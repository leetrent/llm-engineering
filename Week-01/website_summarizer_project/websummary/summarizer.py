import os
from dotenv import load_dotenv
from openai import OpenAI

# Optional: Initialize once at import time (lazy)
client = None

def init_openai():
    global client
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found in .env.")
    client = OpenAI(api_key=api_key)

def summarize_text(text, max_chars=2000, model="gpt-4o"):
    if client is None:
        init_openai()
    
    trimmed = text[:max_chars]
    prompt = f"Please summarize the following webpage text:\n\n{trimmed}"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
