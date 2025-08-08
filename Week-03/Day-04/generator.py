from transformers import AutoTokenizer, TextStreamer, AutoModelForCausalLM
from quant_config import quant_config
import torch
import gc

def generate(model, messages):
  tokenizer = AutoTokenizer.from_pretrained(model)
  tokenizer.pad_token = tokenizer.eos_token
  inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True).to("cuda")
  streamer = TextStreamer(tokenizer)
  model = AutoModelForCausalLM.from_pretrained(model, device_map="auto", quantization_config=quant_config)
  outputs = model.generate(inputs, max_new_tokens=80, streamer=streamer)
  del model, inputs, tokenizer, outputs, streamer
  gc.collect()
  torch.cuda.empty_cache()