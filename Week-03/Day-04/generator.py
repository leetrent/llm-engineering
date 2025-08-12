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

def generate(model_name, messages, max_new_tokens: int = 256):
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

    # Stream live to console, but also capture full output afterwards
    streamer = TextStreamer(tok, skip_prompt=True, skip_special_tokens=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        use_cache=True,
        streamer=streamer,                # live output
        pad_token_id=tok.eos_token_id,
        eos_token_id=tok.eos_token_id,    # early stop if EOS appears
    )

    # Decode the newly generated portion for logging or saving
    input_len = inputs["input_ids"].shape[-1]
    generated = outputs[0][input_len:]
    full_text = tok.decode(generated, skip_special_tokens=True)

    # Optional: print a tidy separator
    print("\n" + "-" * 60 + "\n")  # visual break after stream
    print(full_text)

    # Cleanup
    del model, inputs, tok, outputs, streamer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return full_text
