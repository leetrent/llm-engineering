class LLMMessages:
    def __init__(self):
        self.messages = []
        self._init_system_message()

    def _init_system_message(self):
        self.system_message = "You are a friendly, helpful and honest assistant who answers all questions pertaining to veganism and only veganism in markdown."
        
    def append_assistant_message(self, assistant_message):
        self.messages.append( {"role": "assistant", "content": assistant_message} )
        
    def append_user_message(self, user_message):
        self.messages.append({"role": "user", "content": user_message})