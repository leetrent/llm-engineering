import threading
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextStreamer, TextIteratorStreamer

class Secretary:
    def __init__(self):
        self.model_name = "microsoft/Phi-3-mini-4k-instruct"
        self.max_new_tokens = 2000
        self._set_quant_config()
        self._init_messages()
        
    def _set_quant_config(self):
        self.quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4"
        )
               
    def _set_system_message(self):
        self.system_message = {
            "role": "system",
            "content": ("You produce clear meeting minutes in Markdown: include a brief "
                        "summary with attendees, date, and location; key discussion points; "
                        "decisions; and action items with owners and due dates."),
        }  
        
    def _init_messages(self):
        self._set_system_message()
        self.messages = [self.system_message]
        
    def create_minutes(self, user_prompt):
        self.messages.append(user_prompt)
        
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        tokenizer.pad_token = tokenizer.eos_token
        
        inputs = tokenizer.apply_chat_template(
            self.messages, 
            return_tensors="pt").to("cuda")
        
        streamer = TextStreamer(tokenizer)
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name, 
            device_map="auto", 
            quantization_config=self.quant_config)
        
        outputs = model.generate(inputs, max_new_tokens=self.max_new_tokens, streamer=streamer)
        
        
    def stream_minutes(self, user_prompt):
        self.messages.append(user_prompt)
        
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        tokenizer.pad_token = tokenizer.eos_token
        
        inputs = tokenizer.apply_chat_template(
            self.messages,
            return_tensors="pt"
        ).to("cuda")
        
        streamer = TextIteratorStreamer(
            tokenizer, 
            skip_special_tokens=True
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            quantization_config=self.quant_config
        )
        
        def _do_generate():
            model.generate(
                inputs, 
                max_new_tokens=self.max_new_tokens,
                streamer=streamer
            )

        t = threading.Thread(target=_do_generate)
        t.start()
        
        accumulated = ""
        for token in streamer:
            accumulated += token
            yield accumulated
        
        