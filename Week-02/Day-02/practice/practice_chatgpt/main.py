import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

def _get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found in .env.")
    return api_key
      
def message_gpt(user_prompt):
    try:
        print(f"[main.py][message_gpt] => (user_prompt): '{user_prompt}'")
        openai = OpenAI(api_key=_get_api_key())
        messages = [
            {"role": "system", "content": "You are a helpful assistant that responds in markdown."},
            {"role": "user", "content": user_prompt}
        ]
        stream = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            stream=True
        )
        result = ""
        for chunk in stream:
            result += chunk.choices[0].delta.content or ""
            yield result
    except Exception as e:
        raise RuntimeError(f"Call to OpenAI failed: {e}")
  
def main():
    view = gr.Interface(
        fn=message_gpt,
        inputs=[gr.Textbox(label="Your message:", lines=6)],
        outputs=[gr.Textbox(label="Response:", lines=8)],
        flagging_mode="never"
    ).launch(share=True)
    
if __name__ == "__main__":
  main()