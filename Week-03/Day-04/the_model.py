from transformers import AutoModelForCausalLM

def get_model(model_name, quant_config):
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", quantization_config=quant_config)
    print(model)
    return model