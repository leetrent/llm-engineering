import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebsiteDetails:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    
    def __init__(self, url):
        self.url = url
        self.title = "EMPTY"
        self.text = "EMPTY"
        self.links = []
        self.content = "EMPTY"
        
    def _fetch(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to fetch {self.url}: {exc}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        self._set_title(soup)
        self._set_text(soup)
        self._extract_links(soup)
        self._set_content()
        
    def _set_title(self, soup):
        self.title = soup.title.string if soup.title else "No title found"
        
    def _set_text(self, soup):
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
            
    def _extract_links(self, soup):
        raw_links = (link.get('href') for link in soup.find_all('a'))
        self.links = [urljoin(self.url, href) for href in raw_links if href]
        
    def _set_content(self):
        self.content = f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"