import torch
from transformers import AutoTokenizer, BitsAndBytesConfig

class Secretary:
    def __init__(self):
        self.model_name = "microsoft/Phi-3-mini-4k-instruct"
        self._set_quant_config()
        self.init_messages()
        
    def _set_quant_config(self):
        self.quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4"
        )
        
    def _set_system_message(self):
        message_text = "You are an assistant that produces minutes of meetings from transcripts, with summary, key discussion points, takeaways and action items with owners, in markdown."
        self.system_message = {"role": "system", "content": message_text}
        
    def _init_messages(self):
        self._set_system_message()
        self.messages = [self.system_message]
        
    def create_minutes(self, user_prompt):
        self.messages.append(user_prompt)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)