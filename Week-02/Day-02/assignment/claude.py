import os
from dotenv import load_dotenv
import anthropic

class Claude:
    def __init__(self, system_prompt, user_prompt):
        self.model = "claude-3-haiku-20240307"
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env. for Claude.")
        return api_key

    def stream_response(self):
        try:
            claude = anthropic.Anthropic(api_key=self._get_api_key())
            result = claude.messages.stream(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content":self.user_prompt},
                ],
            )
            response = "<h1>Claude</h1>"
            with result as stream:
                for text in stream.text_stream:
                    response += text or ""
                    yield response
        except Exception as e:
            raise RuntimeError(f"API call to Claude failed: {e}")