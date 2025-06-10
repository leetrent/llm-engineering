import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Sanity check
if not api_key:
    raise RuntimeError("❌ No API key found. Make sure .env contains OPENAI_API_KEY.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Compose and send your first message
message = "Hello, GPT! This is my first ever message to you! Hi!"
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": message}]
)

# Print the response
print("\n🤖 GPT's reply:")
print(response.choices[0].message.content)
