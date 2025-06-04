import sys
import os
from website_details import WebsiteDetails
from brochure_links_prompts import BrochureLinksPrompts
from brochure_creation_prompts import BrochureCreationPrompts
from large_language_model import LargeLanguageModel

def main():
    AI_MODEL = "gpt-4o-mini"

    if len(sys.argv) < 3:
        print("Usage: python brochure_creation_main.py <URL> <COMPANY_NAME>")
        sys.exit(1)

    url = sys.argv[1]
    company_name = sys.argv[2]

    try:
        # WEBSITE LINKS
        website = WebsiteDetails(url)
        website.fetch()

        print("\nWEBSITE LINKS: BEGIN")
        for link in website.links:
            print(link)
        print("WEBSITE LINKS: END")

        # BROCHURE LINKS
        brochure_links_prompts = BrochureLinksPrompts(url, website.links)
        brochure_links = LargeLanguageModel(
            AI_MODEL, brochure_links_prompts.system_prompt, brochure_links_prompts.user_prompt
        ).generate_json_response()

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
        ).generate_text_response()

        print("\nCOMPANY BROCHURE: BEGIN")
        print(company_brochure)
        print("\nCOMPANY BROCHURE: END")

        # SAVE OUTPUT AS MARKDOWN
        save_markdown(company_name, company_brochure)

    except RuntimeError as e:
        print(f"❌ Error: {e}")

def save_markdown(company_name, brochure_text):
    os.makedirs("./output", exist_ok=True)
    filename_base = company_name.replace(" ", "_").lower()
    filepath = f"./output/{filename_base}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(brochure_text)
    print(f"✅ Markdown brochure saved to: {filepath}")

if __name__ == "__main__":
    main()
