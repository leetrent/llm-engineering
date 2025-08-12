models = {
    "PHI3":  "microsoft/Phi-3-mini-4k-instruct",     # ~3.8B params, great quality/speed
    "QWEN2": "Qwen/Qwen2.5-1.5B-Instruct",           # very light, very fast
    "GEMMA2":"google/gemma-2-2b-it",                 # 2B instruct, solid outputs
    "TINY":  "TinyLlama/TinyLlama-1.1B-Chat-v1.0"    # ultra fast fallback
}

def get_model(name):
    key = name.upper()
    if key not in models:
        raise KeyError(f"Model '{name} not found. Available models: {', '.join(models.keys())}")
    return models[key]