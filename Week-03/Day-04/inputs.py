# inputs.py
import torch

def _fold_system_into_user(messages):
    sys_txt = "\n".join(m["content"] for m in messages if m["role"] == "system")
    rest = [m for m in messages if m["role"] != "system"]
    if sys_txt:
        if rest and rest[0]["role"] == "user":
            rest[0] = {"role": "user", "content": f"{sys_txt}\n\n{rest[0]['content']}"}
        else:
            rest.insert(0, {"role": "user", "content": sys_txt})
    return rest

def _apply(tokenizer, msgs):
    return tokenizer.apply_chat_template(
        msgs,
        add_generation_prompt=True,
        return_tensors="pt",
    )

def get_inputs(tokenizer, messages):
    # First try as-is
    try:
        input_ids = _apply(tokenizer, messages)
    except Exception as e:
        # If template rejects `system`, fold system into the first user message and retry
        if "System role not supported" in str(e):
            folded = _fold_system_into_user(messages)
            input_ids = _apply(tokenizer, folded)
        else:
            raise

    attention_mask = torch.ones_like(input_ids)  # no padding used
    return {"input_ids": input_ids, "attention_mask": attention_mask}
