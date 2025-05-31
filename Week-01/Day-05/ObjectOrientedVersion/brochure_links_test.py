import sys
from website import Website
from large_language_model import LargeLanguageModel

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_site.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        # WEBSITE LINKS
        website = Website(url)
        website._fetch_and_parse()
        
        print("\nWEBSITE LINKS: BEGIN")
        for link in website.links:
            print(link)
        print("WEBSITE LINKS: END")
        
        # BROCHURE LINKS
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt(website.url, website.links)
        brochure_links = LargeLanguageModel("gpt-4o-mini", system_prompt, user_prompt)._create_completions_in_json()
        
        print("\nBROCHURE LINKS: BEGIN")
        print(brochure_links)
        print("BROCHURE LINKS: END")
    except RuntimeError as e:
        print(f"❌ Error: {e}")

def get_system_prompt():
    system_prompt = "You are provided with a list of links found on a webpage. \
    You are able to decide which of the links would be most relevant to include in a brochure about the company, \
    such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    system_prompt += "You should respond in JSON as in this example:"
    system_prompt += """
    {
        "links": [
            {"type": "about page", "url": "https://full.url/goes/here/about"},
            {"type": "careers page": "url": "https://another.full.url/careers"}
        ]
    }
    """
    return system_prompt

def get_user_prompt(url, website_links):
    user_prompt = f"Here is the list of links on the website of {url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website_links)
    return user_prompt

if __name__ == "__main__":
    main()
