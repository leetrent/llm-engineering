import sys
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
from api_key import retrieve_api_key_value

def generate_image(p_prompt):
    openai = OpenAI(api_key=retrieve_api_key_value("OPENAI_API_KEY"))
    image_response = openai.images.generate(
            model="dall-e-3",
            prompt=p_prompt,
            size="1024x1024",
            n=1,
            response_format="b64_json",
        )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

def main():
    if len(sys.argv) < 2:
        print("Usage: python image.py <DESTINATION>")
        sys.exit(1)

    destination = sys.argv[1]
    prompt=f"An image, in an vibrant pop-art style, representing a vacation in {destination}, showing tourist spots and everything unique about {destination}."
    image = generate_image(prompt)
    image.show()
    
if __name__ == "__main__":
  main()