import os
import argparse
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
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
    # 🧾 Parse command-line argument
    parser = argparse.ArgumentParser(description="Scrape and summarize a webpage")
    parser.add_argument("url", help="The URL of the website to summarize")
    args = parser.parse_args()

    # 🌐 Scrape
    site = Website(args.url)

    print(f"\n🌐 Title: {site.title}")
    print("🧠 Summarizing page content using GPT-4o...")

    prompt = f"Please summarize the following webpage text:\n\n{site.text[:2000]}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content

    print(f"\n📄 Summary:\n{summary}")

    # 💾 Save to file (name based on domain)
    domain = site.url.split("//")[-1].split("/")[0]
    filename = f"{domain.replace('.', '_')}_summary.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"🌐 Title: {site.title}\n\n")
        file.write("📄 Raw Page Text:\n")
        file.write(site.text)
        file.write("\n\n🧠 GPT-4o Summary:\n")
        file.write(summary)

    print(f"\n✅ Full content and summary saved to: {filename}")
