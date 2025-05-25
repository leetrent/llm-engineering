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
    #client = OpenAI(api_key=api_key)
    client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

def summarize_text(text, max_chars=2000, model="llama3.2"):
    if client is None:
        init_openai()
    
    trimmed = text[:max_chars]
    
    system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."
    user_prompt = f"Please summarize the following webpage text:\n\n{trimmed}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content
