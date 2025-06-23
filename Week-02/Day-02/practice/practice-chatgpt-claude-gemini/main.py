import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai as genai
import gradio as gr

def _get_api_key(api_key):
    load_dotenv(override=True)
    api_key = os.getenv(api_key)
    if not api_key:
        raise RuntimeError("❌ No API key found in .env.")
    return api_key

def stream_chatgpt(user_prompt):
    try:
        print(f"[main.py][message_gpt] => (user_prompt): '{user_prompt}'")
        openai = OpenAI(api_key=_get_api_key("OPENAI_API_KEY"))
        messages = [
            {"role": "system", "content": "You are a helpful assistant that responds in markdown."},
            {"role": "user", "content": user_prompt}
        ]
        stream = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            stream=True
        )
        result = "<H1>ChatGPT</H1>"
        for chunk in stream:
            result += chunk.choices[0].delta.content or ""
            yield result
    except Exception as e:
        raise RuntimeError(f"Call to OpenAI failed: {e}")
    
def stream_claude(user_prompt):
    try:
        print(f"[main.py][stream_claude] => (user_prompt): '{user_prompt}'")
        claude = anthropic.Anthropic(api_key=_get_api_key("ANTHROPIC_API_KEY"))
        result = claude.messages.stream(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.7,
            system="You are a helpful assistant who responds using markdown.",
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        response = "<H1>Claude</H1>"
        with result as stream:
            for text in stream.text_stream:
                response += text or ""
                yield response
    except Exception as e:
        raise RuntimeError(f"Call to Claude failed: {e}")
    
def stream_gemini(user_prompt):
    print(f"[main.py][stream_gemini] => (user_prompt): '{user_prompt}'")
    """
    Makes a streaming API call to the Gemini model and yields the response in chunks.
    """
    try:
        print(f"[main-gemini.py][stream_gemini] => (user_prompt): '{user_prompt}'")

        # Configure the generative AI model with your API key
        genai.configure(api_key=_get_api_key("GEMINI_API_KEY"))

        # Initialize the Gemini Pro model
        # For streaming, 'gemini-pro' is a good choice. 'gemini-1.5-flash' also supports streaming.
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Start a chat session (important for multi-turn conversations if you expand this)
        # For a single turn, generate_content directly also works.
        chat = model.start_chat(history=[])

        # Generate content with streaming enabled
        response_stream = chat.send_message(user_prompt, stream=True)

        result = "<H1>Gemini</H1>"
        # Iterate through the streamed response chunks
        for chunk in response_stream:
            result += chunk.text
            yield result # Yield each chunk to Gradio
    except Exception as e:
        raise RuntimeError(f"Call to Gemini failed: {e}")
    
def stream_model(user_prompt, model):
    print(f"[main.py][stream_model] => (model)......: '{model}'")
    print(f"[main.py][stream_model] => (user_prompt): '{user_prompt}'")
    
    if model=="ChatGPT":
        result = stream_chatgpt(user_prompt)
    elif model=="Claude":
        result = stream_claude(user_prompt)
    elif model=="Gemini":
        result = stream_gemini(user_prompt)
    else:
        raise ValueError("Unknown model")
    
    yield from result
    
def main():
    gr.Interface(
        fn=stream_model,
        inputs=[gr.Textbox(label="Your message:"), gr.Dropdown(["ChatGPT", "Claude", "Gemini"], label="Select model", value="ChatGPT")],
        outputs=[gr.Markdown(label="Response:")],
        flagging_mode="never"
    ).launch(share=True)
        
if __name__ == "__main__":
    main()