import sys
import torch
from diffusers import FluxPipeline
from huggingface_hub import login
from api_key import retrieve_api_key_value

def generate_image(prompt):
    print(f"🧠 Prompt: {prompt}")
    print(f"🚀 Using device: {'cuda' if torch.cuda.is_available() else 'cpu'}")

    # Authenticate with Hugging Face
    login(retrieve_api_key_value("HF_TOKEN"), add_to_git_credential=True)

    torch.cuda.empty_cache()   
    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16).to("cuda")
    generator = torch.Generator(device="cuda").manual_seed(0)
    prompt = "A futuristic class full of students learning AI coding in the surreal style of Salvador Dali"

    # Generate the image using the GPU
    image = pipe(
        prompt,
        guidance_scale=0.0,
        num_inference_steps=4,
        max_sequence_length=256,
        generator=generator
    ).images[0]
    
    return image

def main():
    if len(sys.argv) < 2:
        print("Usage: python image_gen_v1.py \"<PROMPT TEXT>\"")
        sys.exit(1)

    prompt = sys.argv[1]
    image = generate_image(prompt)
    image.save("generated_image-v2.png")
    print("✅ Image saved as generated_image.png")

if __name__ == "__main__":
    main()
