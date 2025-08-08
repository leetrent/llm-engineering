from transformers import AutoModelForCausalLM
from quant_config import quant_config

model = AutoModelForCausalLM.from_pretrained(LLAMA, device_map="auto", quantization_config=quant_config)