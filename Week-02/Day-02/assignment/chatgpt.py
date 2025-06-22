import os
from dotenv import load_dotenv
from openai import OpenAI

class ChatGPT:
    def __init__(self, system_prompt, user_prompt):
        self.model = "gpt-4o-mini"
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

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
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}
                ],
                stream=True
            )
            result = "<h1>ChatGPT</h1>"
            for chunk in stream:
                result += chunk.choices[0].delta.content or ""
                yield result
        except Exception as e:
            raise RuntimeError(f"API call to ChatGPT failed: {e}")
        
