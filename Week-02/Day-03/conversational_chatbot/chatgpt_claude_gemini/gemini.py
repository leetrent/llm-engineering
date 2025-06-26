import os
from dotenv import load_dotenv
import google.generativeai as genai

class Gemini:
    def __init__(self, system_message, user_assistant_messages):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.system_message = system_message
        self.user_assistant_messages = user_assistant_messages
        
        print("\nGemini Constructor:")
        print(user_assistant_messages)

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
                system_instruction=self.system_message)
            
            # Separate history and last message
            history = self.user_assistant_messages[:-1]  # everything except the last
            last_message = self.user_assistant_messages[-1]  # latest user message
            
            chat = model.start_chat(history=history)

            # Generate content with streaming enabled
            response_stream = chat.send_message(
                parts=last_message["parts"],
                stream=True
            )

            result = "<h1>Gemini</h1>"
            # Iterate through the streamed response chunks
            for chunk in response_stream:
                result += chunk.text
                yield result # Yield each chunk to Gradio
        except Exception as e:
            raise RuntimeError(f"API call to Gemini failed: {e}")