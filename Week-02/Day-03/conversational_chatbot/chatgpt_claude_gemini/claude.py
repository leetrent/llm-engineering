import os
from dotenv import load_dotenv
import anthropic

class Claude:       
    def __init__(self, sys_msg, msg_hist, curr_msg):
        self.model = "claude-3-haiku-20240307"
        self.system_message = sys_msg
        self.message_history = msg_hist
        self.current_message = curr_msg
        self.nonsystem_messages = self._prepare_nonsystem_messages()
        
        # print("\nCLAUDE (system_message)")
        # print(self.system_message)
        # print("\nCLAUDE (message_history)")
        # print(self.message_history)
        # print("\nCLAUDE (current_message)")
        # print(self.current_message)  

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
                system=self.system_message,
                messages=self.nonsystem_messages
            )
            response = ""
            with result as stream:
                for text in stream.text_stream:
                    response += text or ""
                    yield response
        except Exception as e:
            raise RuntimeError(f"API call to Claude failed: {e}")
        
    def _prepare_nonsystem_messages(self):
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in self.message_history + [{"role": "user", "content": self.current_message}]
        ]