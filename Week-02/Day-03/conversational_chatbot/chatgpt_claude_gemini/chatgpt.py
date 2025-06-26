import os
from dotenv import load_dotenv
from openai import OpenAI

class ChatGPT:
    def __init__(self, messages):
        self.model = "gpt-4o-mini"
        self.messages = messages

    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env for ChatGPT.")
        return api_key
    
    def stream_response(self):
        try:
            openai_client = OpenAI(api_key=self._get_api_key())
            stream = openai_client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
            result = "<h1>ChatGPT</h1>"
            for chunk in stream:
                result += chunk.choices[0].delta.content or ""
                yield result
        except Exception as e:
            raise RuntimeError(f"API call to ChatGPT failed: {e}")
        
