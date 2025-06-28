class LLMMessages:
    def __init__(self, msg_hist, curr_msg):
        self._init_system_message()
        self.message_history = msg_hist
        self.current_message = curr_msg

    def _init_system_message(self):
        self.system_message = "You are a friendly, helpful and honest assistant who answers all questions pertaining to veganism and only veganism in markdown."
        
    def for_chatgpt(self):    
        all_messages = [{"role": "system", "content": self.system_message}] + self.message_history + [{"role": "user", "content": self.current_message}]
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in all_messages
        ]
    
    def for_claude(self):
        user_assistant_messages = self.message_history + [{"role": "user", "content": self.current_message}]
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in user_assistant_messages
        ]  
        
    def for_gemini(self):
        user_assistant_messages = self.message_history + [{"role": "user", "content": self.current_message}]
        return [
            {
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            }
            for msg in user_assistant_messages
        ]     
