import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variable
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ No API key found in .env.")

client = OpenAI(api_key=api_key)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
}

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string.strip() if soup.title else "No title found"
        for tag in soup.body(["script", "style", "img", "input"]):
            tag.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

if __name__ == "__main__":
    ed = Website("https://edwarddonner.com")

    print(f"\n🌐 Title: {ed.title}")
    print("\n🧠 Summarizing page content using GPT-4o...")

    # Limit to first 2000 characters to stay well within token limits
    prompt = f"Please summarize the following webpage text:\n\n{ed.text[:2000]}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content
    print(f"\n📄 Summary:\n{summary}")
