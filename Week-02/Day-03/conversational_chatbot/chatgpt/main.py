import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

def _get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found for OpenAI in .env.")
    return api_key
      
def chat_with_gpt(message, history):
    try:
        print(f"[main.py][chat_with_gpt] => (message):")
        print(message)  
            
        print(f"\n[main.py][chat_with_gpt] => (history):")  
        for hist in history:
            print(f"Role: {hist['role']},\nContent: {hist['content']}")
        print("")
        
        system_message = "You are a friendly, helpful and honest assistant who answers all questions pertaining to veganism and only veganism and responds in markdown."
        messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
        openai = OpenAI(api_key=_get_api_key())
        stream = openai.chat.completions.create(model='gpt-4o-mini', messages=messages, stream=True)

        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            yield response
    except Exception as e:
        raise RuntimeError(f"Call to OpenAI failed: {e}")
  
def main():
    gr.ChatInterface(fn=chat_with_gpt, type="messages").launch()
    
if __name__ == "__main__":
  main()