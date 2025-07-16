import sys
import torch
from diffusers import StableDiffusionPipeline
from huggingface_hub import login
from api_key import retrieve_api_key_value

def generate_image(prompt):
    print(f"🧠 Prompt: {prompt}")
    print(f"🚀 Using device: {'cuda' if torch.cuda.is_available() else 'cpu'}")

    # Authenticate with Hugging Face
    login(retrieve_api_key_value("HF_TOKEN"), add_to_git_credential=True)

    # Load model with CUDA acceleration
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    ).to("cuda")

    # Generate image with guidance
    image = pipe(
        prompt=prompt,
        guidance_scale=7.5,          # Enforce prompt more strongly
        num_inference_steps=50       # More steps = higher quality
    ).images[0]

    return image

def main():
    if len(sys.argv) < 2:
        print("Usage: python image_gen.py \"<PROMPT TEXT>\"")
        sys.exit(1)

    prompt = sys.argv[1]
    image = generate_image(prompt)
    image.save("generated_image.png")
    print("✅ Image saved as generated_image.png")

if __name__ == "__main__":
    main()
