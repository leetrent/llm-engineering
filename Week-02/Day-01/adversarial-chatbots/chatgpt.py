import os
from dotenv import load_dotenv
from openai import OpenAI

class ChatGPT:
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.messages = []
        self._append_system_message()
        
    def _append_system_message(self):
        system_prompt = "You are a chatbot who is very argumentative. "\
            "You disagree with anything in the conversation and you challenge everything, in a snarky way."       
        self.messages =  [{"role": "system", "content": system_prompt}]
        
    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env.")
        return api_key
            
    def append_assistant_message(self, assistant_message):
        self.messages.append( {"role": "assistant", "content": assistant_message} )
        
    def append_user_message(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        
    def generate_text_response(self):
        try:
            openai_client = OpenAI(api_key=self._get_api_key())
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI text completion failed: {e}")
            