import os
from dotenv import load_dotenv
import ollama

def summarize_text(text, max_chars=2000, model="llama3.2"):   
    print(f"summarizer.py will be using {model}")
    
    trimmed = text[:max_chars]
    
    system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."
    user_prompt = f"Please summarize the following webpage text:\n\n{trimmed}"

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    #return response.choices[0].message.content
    return response['message']['content']
