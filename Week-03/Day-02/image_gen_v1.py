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

    # Load the Stable Diffusion pipeline with FP16 precision on GPU
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    ).to("cuda")

    # Optimize memory usage for 4GB GPU
    pipe.enable_attention_slicing()

    # Debugging aid — confirm model is on GPU
    print(f"🕵️ UNet is on device: {pipe.unet.device}")

    # Generate image
    image = pipe(
        prompt=prompt,
        guidance_scale=7.5,
        num_inference_steps=50
    ).images[0]

    return image

def main():
    if len(sys.argv) < 2:
        print("Usage: python image_gen_v1.py \"<PROMPT TEXT>\"")
        sys.exit(1)

    prompt = sys.argv[1]
    image = generate_image(prompt)
    image.save("generated_image.png")
    print("✅ Image saved as generated_image.png")

if __name__ == "__main__":
    main()
