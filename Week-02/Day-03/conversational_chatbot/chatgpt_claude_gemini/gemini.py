import os
from dotenv import load_dotenv
import google.generativeai as genai

class Gemini:       
    def __init__(self, sys_msg, msg_hist, curr_msg):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.system_message = sys_msg
        self.message_history = self._convert_for_gemini(msg_hist)
        # self.current_message = self._convert_for_gemini(curr_msg)
        self.current_message = curr_msg
        
        print("\nGEMINI (system_message)")
        print(self.system_message)
        print("\nGEMINI (message_history)")
        print(self.message_history)
        print("\nGEMINI (current_message)")
        print(self.current_message)    

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
            
            chat = model.start_chat(history=self.message_history)

            # Generate content with streaming enabled
            response_stream = chat.send_message(
                content=self.current_message,
                stream=True
            )

            result = ""
            # Iterate through the streamed response chunks
            for chunk in response_stream:
                result += chunk.text
                yield result # Yield each chunk to Gradio
        except Exception as e:
            raise RuntimeError(f"API call to Gemini failed: {e}")
        
    def _convert_for_gemini(self, messages):
        return [
            {
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            }
            for msg in messages
        ]