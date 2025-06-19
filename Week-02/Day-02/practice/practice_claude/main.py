import os
from dotenv import load_dotenv
import anthropic
import gradio as gr

def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found for Anthropic in .env.")
    return api_key
         
def stream_claude(user_prompt):
    try:
        print(f"[main.py][stream_claude] => (user_prompt): '{user_prompt}'")
        claude = anthropic.Anthropic(api_key=get_api_key())
        result = claude.messages.stream(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.7,
            system="You are a helpful assistant who responds using markdown.",
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        response = ""
        with result as stream:
            for text in stream.text_stream:
                response += text or ""
                yield response
    except Exception as e:
        raise RuntimeError(f"Call to Claude failed: {e}")
  
def main():
    view = gr.Interface(
        fn=stream_claude,
        inputs=[gr.Textbox(label="Your message:", lines=6)],
        outputs=[gr.Textbox(label="Response:", lines=8)],
        flagging_mode="never"
    ).launch(share=True)
    
if __name__ == "__main__":
  main()