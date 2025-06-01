import os
from dotenv import load_dotenv
from openai import OpenAI
import json

class LargeLanguageModel:
    def __init__(self, p_model, p_system_prompt, p_user_prompt):
        self.model = p_model
        self.system_prompt = p_system_prompt
        self.user_prompt = p_user_prompt
        
    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env.")
        return api_key

    def _create_completions_in_json(self):
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

    def _create_completions(self):
        openai_client = OpenAI(api_key=self._get_api_key())
        response = openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.user_prompt}
        ],
        )
        return response.choices[0].message.content
   