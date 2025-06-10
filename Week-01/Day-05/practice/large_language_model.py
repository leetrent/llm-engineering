import os
import json
from dotenv import load_dotenv
from openai import OpenAI

class LargeLanguageModel:
    def __init__(self, model, system_prompt, user_prompt):
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env.")
        return api_key

    def generate_json_response(self):
        try:
            openai_client = OpenAI(api_key=self._get_api_key())
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            raise RuntimeError(f"OpenAI JSON completion failed: {e}")

    def generate_text_response(self):
        try:
            openai_client = OpenAI(api_key=self._get_api_key())
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI text completion failed: {e}")

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
            for chunch in stream:
                print(chunch.choices[0].delta.content or '', end='')
        except Exception as e:
            raise RuntimeError(f"OpenAI text completion failed: {e}")