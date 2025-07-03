import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
from io import BytesIO
from PIL import Image

def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found for OpenAI in .env.")
    return api_key

def artist(city):
    openai = OpenAI(api_key=get_api_key())
    image_response = openai.images.generate(
            model="dall-e-3",
            prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
            size="1024x1024",
            n=1,
            response_format="b64_json",
        )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

def main():
    image = artist("Chicago")
    image.show()
    
if __name__ == "__main__":
  main()