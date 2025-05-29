import sys
from website_links import get_links_from_url
from brochure_links import get_brochure_links_from_website_links

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_website_links.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        # WEBSITE LINKS
        website_links = get_links_from_url(url)
        print("\nWEBSITE LINKS: BEGIN")
        for website_link in website_links:
            print(website_link)
        print("WEBSITE LINKS: END")
        
        # BROCHURE LINKS
        brochure_links = get_brochure_links_from_website_links(url, website_links)
        print("\nBROCHURE LINKS: BEGIN")
        print(brochure_links)
        print("BROCHURE LINKS: END")
    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
