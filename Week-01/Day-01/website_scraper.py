import requests
from bs4 import BeautifulSoup

# Use headers to simulate a browser (some sites reject bots)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
}

class Website:
    def __init__(self, url):
        """
        Create a Website object from the given URL using BeautifulSoup.
        Cleans up <script>, <style>, <img>, and <input> elements.
        """
        self.url = url
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # raises error if site is unreachable

        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string.strip() if soup.title else "No title found"

        # Remove unwanted tags from body
        for tag in soup.body(["script", "style", "img", "input"]):
            tag.decompose()

        # Extract text from body
        self.text = soup.body.get_text(separator="\n", strip=True)

if __name__ == "__main__":
    ed = Website("https://edwarddonner.com")
    print(f"\n🌐 Title:\n{ed.title}")
    print(f"\n📄 Body Text Preview (first 500 characters):\n{ed.text[:500]}")
