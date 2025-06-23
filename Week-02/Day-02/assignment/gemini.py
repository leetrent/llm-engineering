import os
from dotenv import load_dotenv
import google.generativeai as genai

class Gemini:
    def __init__(self, system_prompt, user_prompt):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env. for Gemini.")
        return api_key

    def stream_response(self):
        try:
            genai.configure(api_key=self._get_api_key())
            
            model = genai.GenerativeModel(
                'gemini-1.5-flash',
                system_instruction=self.system_prompt)
            
            chat = model.start_chat(history=[])

            # Generate content with streaming enabled
            response_stream = chat.send_message(self.user_prompt, stream=True)

            result = "<h1>Gemini</h1>"
            # Iterate through the streamed response chunks
            for chunk in response_stream:
                result += chunk.text
                yield result # Yield each chunk to Gradio
        except Exception as e:
            raise RuntimeError(f"API call to Gemini failed: {e}")