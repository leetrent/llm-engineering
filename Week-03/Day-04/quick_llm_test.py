# save as quick_llm_test.py and run: python quick_llm_test.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

print("GPU:", torch.cuda.get_device_name(0))
free, total = torch.cuda.mem_get_info()
print(f"VRAM free/total: {free/1e9:.2f} / {total/1e9:.2f} GB")

# 4-bit quantization (best for 4GB cards)
bnb_cfg = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model_id = "Qwen/Qwen2.5-1.5B-Instruct"  # small, solid, fits in 4GB at 4-bit
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=bnb_cfg,
    torch_dtype=torch.bfloat16,
)

prompt = "You are a helpful assistant. Briefly explain why the sky is blue."
inputs = tok(prompt, return_tensors="pt").to(model.device)
out = model.generate(**inputs, max_new_tokens=80)
print(tok.decode(out[0], skip_special_tokens=True))
