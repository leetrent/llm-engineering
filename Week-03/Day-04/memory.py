def print_memory(model):
    memory = model.get_memory_footprint() / 1e6
    print(f"Memory footprint: {memory:,.1f} MB")