import sys
from website import Website

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_site.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        site = Website(url)
        site._fetch_and_parse()
        
        # URL
        print("\nURL:", site.url)
        
        # TITLE
        print("\nTitle:", site.title)
        
       # TEXT
        print("\nText:", site.text)
        
        # LINKS
        print("\nLINKS: BEGIN")
        for link in site.links:
            print(link)
        print("LINKS: END")
        
        # CONTENT
        print("\nCONTENT: BEGIN")
        print("Content", site.content)
        print("CONTENT: END")
    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
