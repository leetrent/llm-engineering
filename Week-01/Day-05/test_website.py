import sys
from website import Website

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_site.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        site = Website(url)
        for link in site.links:
            print(link)
    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
