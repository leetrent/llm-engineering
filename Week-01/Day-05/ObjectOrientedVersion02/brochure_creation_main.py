import sys
from website_details import WebsiteDetails
from brochure_links_prompts import BrochureLinksPrompts
from brochure_creation_prompts import BrochureCreationPrompts
from large_language_model import LargeLanguageModel

def main():
    AI_MODEL = "gpt-4o-mini"

    if len(sys.argv) < 3:
        print("Usage: expected two arguments <URL> <COMPANY_NAME>")
        sys.exit(1)

    url = sys.argv[1]
    company_name = sys.argv[2]

    try:
        # WEBSITE LINKS
        website = WebsiteDetails(url)
        website._fetch()

        print("\nWEBSITE LINKS: BEGIN")
        for link in website.links:
            print(link)
        print("WEBSITE LINKS: END")

        # BROCHURE LINKS
        brochure_links_prompts = BrochureLinksPrompts(url, website.links)
        brochure_links = LargeLanguageModel(
            AI_MODEL, brochure_links_prompts.system_prompt, brochure_links_prompts.user_prompt
        )._create_completions_in_json()

        print("\nBROCHURE LINKS: BEGIN")
        print(brochure_links)
        print("BROCHURE LINKS: END")

        # ENRICH LINKS WITH CONTENT
        for link in brochure_links["links"]:
            try:
                enriched = WebsiteDetails(link["url"])
                enriched.fetch()
                link["content"] = enriched.content
            except Exception as e:
                link["content"] = "[Error fetching content]"

        # BROCHURE CREATION
        brochure_creation_prompts = BrochureCreationPrompts(
            company_name, website.content, brochure_links
        )

        company_brochure = LargeLanguageModel(
            AI_MODEL, brochure_creation_prompts.system_prompt, brochure_creation_prompts.user_prompt
        )._create_completions()

        print("\nCOMPANY BROCHURE: BEGIN")
        print(company_brochure)
        print("\nCOMPANY BROCHURE: END")

    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
