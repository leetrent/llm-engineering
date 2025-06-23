import os
from dotenv import load_dotenv
import google.generativeai as genai
import gradio as gr

def _get_api_key():
    """
    Loads the Gemini API key from the .env file.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY") # Ensure your .env has GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("❌ No API key found for Gemini in .env. Please set GEMINI_API_KEY.")
    return api_key

def stream_gemini(user_prompt):
    """
    Makes a streaming API call to the Gemini model and yields the response in chunks.
    """
    try:
        print(f"[main-gemini.py][stream_gemini] => (user_prompt): '{user_prompt}'")

        # Configure the generative AI model with your API key
        genai.configure(api_key=_get_api_key())

        # Initialize the Gemini Pro model
        # For streaming, 'gemini-pro' is a good choice. 'gemini-1.5-flash' also supports streaming.
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Start a chat session (important for multi-turn conversations if you expand this)
        # For a single turn, generate_content directly also works.
        chat = model.start_chat(history=[])

        # Generate content with streaming enabled
        response_stream = chat.send_message(user_prompt, stream=True)

        result = ""
        # Iterate through the streamed response chunks
        for chunk in response_stream:
            result += chunk.text
            yield result # Yield each chunk to Gradio
    except Exception as e:
        raise RuntimeError(f"Call to Gemini failed: {e}")

def main():
    """
    Sets up and launches the Gradio interface for interacting with Gemini.
    """
    view = gr.Interface(
        fn=stream_gemini,
        inputs=[gr.Textbox(label="Your message (Gemini):", lines=6)],
        outputs=[gr.Textbox(label="Gemini Response:", lines=8)],
        title="Gemini LLM Chatbot",
        description="Interact with the Google Gemini Pro model.",
        flagging_mode="never"
    ).launch(share=True) # share=True allows you to share the link publicly

if __name__ == "__main__":
    main()
