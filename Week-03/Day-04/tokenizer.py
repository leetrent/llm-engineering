from transformers import AutoTokenizer

def get_tokenizer(model):
    tokenizer = AutoTokenizer.from_pretrained(model)
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer

#inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")