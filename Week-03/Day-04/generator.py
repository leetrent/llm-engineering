import gc
import torch
from transformers import TextStreamer, AutoModelForCausalLM
from tokenizer import get_tokenizer
from inputs import get_inputs
from quant_config import get_config

def _to_device(batch, device):
    if isinstance(batch, dict):
        return {k: (v.to(device) if hasattr(v, "to") else v) for k, v in batch.items()}
    return batch.to(device) if hasattr(batch, "to") else batch

def generate(model_name, messages):
    tok = get_tokenizer(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=get_config(),
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )

    inputs = get_inputs(tok, messages)
    dev = next(model.parameters()).device
    inputs = _to_device(inputs, dev)

    streamer = TextStreamer(tok, skip_prompt=True, skip_special_tokens=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        use_cache=True,
        streamer=streamer,
        pad_token_id=tok.eos_token_id, 
        eos_token_id=tok.eos_token_id,
    )

    del model, inputs, tok, outputs, streamer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
