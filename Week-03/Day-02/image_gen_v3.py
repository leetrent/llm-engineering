import sys
import torch
from diffusers import StableDiffusionPipeline

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"🧠 Prompt: {prompt}")

    # Determine the best device available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Using device: {device}")

    # Use a model that's compatible with 4GB VRAM GPUs
    model_id = "CompVis/stable-diffusion-v1-4"

    # Load the pipeline
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)

    # Try enabling memory-efficient attention if xformers is available
    try:
        pipe.enable_xformers_memory_efficient_attention()
    except Exception as e:
        print(f"⚠️ xformers not enabled: {e}")

    # Send pipeline to appropriate device
    pipe = pipe.to(device)

    # Generate the image
    image = pipe(prompt).images[0]

    # Save the image
    output_filename = "generated_image.png"
    image.save(output_filename)
    print(f"✅ Image saved as {output_filename}")

if __name__ == "__main__":
    main()
