import sys
from website_links import get_links_from_url

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_website_links.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        links = get_links_from_url(url)
        for link in links:
            print(link)
    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
