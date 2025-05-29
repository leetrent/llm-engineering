import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def get_links_from_url(url, timeout=30):
    """
    Fetch all anchor links from the given URL and return them as a list.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch {url}: {exc}")

    soup = BeautifulSoup(response.content, 'html.parser')
    raw_links = (link.get('href') for link in soup.find_all('a'))
    return [urljoin(url, href) for href in raw_links if href]
