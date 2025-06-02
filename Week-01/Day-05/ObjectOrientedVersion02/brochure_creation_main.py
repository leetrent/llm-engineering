import sys
from website_details import WebsiteDetails
from brochure_links_prompts import BrochureLinksPrompts
from large_language_model import LargeLanguageModel

def main():
    AI_MODEL = "gpt-4o-mini"
    
    if len(sys.argv) < 3:
        print("Usage: expcted two arguments <URL>, <COMPANY_NAME>")
        sys.exit(1)

    url = sys.argv[1]
    company_name = sys.argv[2]
    
    try:
        # WEBSITE LINKS
        website = WebsiteDetails(url)
        website._fetch_and_parse()
        
        print("\nWEBSITE LINKS: BEGIN")
        for link in website.links:
            print(link)
        print("WEBSITE LINKS: END")
        
        # BROCHURE LINKS
        brochure_links_prompts = BrochureLinksPrompts(url, website.links)
        brochure_links = LargeLanguageModel("gpt-4o-mini", brochure_links_prompts.system_prompt, brochure_links_prompts.user_prompt)._create_completions_in_json()
        
        print("\nBROCHURE LINKS: BEGIN")
        print(brochure_links)
        print("BROCHURE LINKS: END")
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        
        
if __name__ == "__main__":
    main()