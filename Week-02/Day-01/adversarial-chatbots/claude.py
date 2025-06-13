import os
from dotenv import load_dotenv
import anthropic

class Claude:
    def __init__(self):
        self.model = "claude-3-haiku-20240307"
        self.messages = []
        self._set_system_prompt()
        
    def _set_system_prompt(self):
        self.system_prompt = "You are a very polite, courteous chatbot. "\
            "You try to agree with everything the other person says, or find common ground. "\
            "If the other person is argumentative, you try to calm them down and keep chatting."     
        
    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env.")
        return api_key
            
    def append_assistant_message(self, assistant_message):
        self.messages.append( {"role": "assistant", "content": assistant_message} )
        
    def append_user_message(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        
    def generate_text_response(self):
        try:
            claude = anthropic.Anthropic(api_key=self._get_api_key())
            response = claude.messages.create(
                model=self.model,
                system=self.system_prompt,
                messages=self.messages,
                max_tokens=500
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic Claude text completion failed: {e}")
            