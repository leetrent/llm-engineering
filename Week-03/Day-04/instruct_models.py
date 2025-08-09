# Define the dictionary with keys in uppercase
models = {
    "LLAMA": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "PHI3": "microsoft/Phi-3-mini-4k-instruct",
    "GEMMA2": "google/gemma-2-2b-it",
    "QWEN2": "Qwen/Qwen2-7B-Instruct",  # exercise for you
    "MIXTRAL": "mistralai/Mixtral-8x7B-Instruct-v0.1"  # If this doesn't fit in your GPU memory, try others from the hub
}

def get_model(name):
    key = name.upper()
    if key not in models:
        raise KeyError(f"Model '{name} not found. Available models: {', '.join(models.keys())}")
    return models[key]