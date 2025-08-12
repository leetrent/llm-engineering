import torch

def get_inputs(tokenizer, messages):
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    attention_mask = torch.ones_like(input_ids)  # no padding -> all ones
    return {"input_ids": input_ids, "attention_mask": attention_mask}
