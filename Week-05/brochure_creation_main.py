import sys
import os
from website_details import WebsiteDetails
from brochure_links_prompts import BrochureLinksPrompts
from brochure_creation_prompts import BrochureCreationPrompts
from large_language_model import LargeLanguageModel
from language_translation_prompts import LanguageTranslationPrompts

def main():
    AI_MODEL = "gpt-4o-mini"
    TARGET_LANGUAGE = "Hindi"

    if len(sys.argv) < 3:
        print("Usage: python brochure_creation_main.py <URL> <COMPANY_NAME>")
        sys.exit(1)

    url = sys.argv[1]
    company_name = sys.argv[2]

    try:
        ################################################################################
        # WEBSITE LINKS
        ################################################################################
        print("\n\nProcessing all website links ...\n")
        website = WebsiteDetails(url)
        website.fetch()

        #print("\nWEBSITE LINKS: BEGIN")
        for link in website.links:
            print(link)
        #print("WEBSITE LINKS: END")
        print("\n\nDone processing all website links ...\n")

        ################################################################################
        # BROCHURE LINKS
        ################################################################################
        print("\n\nProcessing all brochure links ...\n")
        brochure_links_prompts = BrochureLinksPrompts(url, website.links)
        brochure_links = LargeLanguageModel(
            AI_MODEL, brochure_links_prompts.system_prompt, brochure_links_prompts.user_prompt
        ).generate_json_response()

        # print("\nBROCHURE LINKS: BEGIN")
        # print(brochure_links)
        # print("\n")
        # for link in brochure_links["links"]:
        #     print(link["type"], ' - ', link["url"])
        # print("\n")
        # print("BROCHURE LINKS: END")

        # ENRICH LINKS WITH CONTENT
        for link in brochure_links["links"]:
            try:
                enriched = WebsiteDetails(link["url"])
                enriched.fetch()
                link["content"] = enriched.content
            except Exception as e:
                link["content"] = "[Error fetching content]"
        print("\n\nDone processing all brochure links ...\n")
        
        ################################################################################
        # BROCHURE CREATION
        ################################################################################
        print ("\n\nCreating company brochure...\n")
        
        brochure_creation_prompts = BrochureCreationPrompts(
            company_name, website.content, brochure_links
        )

        llm = LargeLanguageModel(
            AI_MODEL, brochure_creation_prompts.system_prompt, brochure_creation_prompts.user_prompt)
        llm.stream_response()

        company_brochure = LargeLanguageModel(
            AI_MODEL, brochure_creation_prompts.system_prompt, brochure_creation_prompts.user_prompt
        ).generate_text_response()

        # print("\nCOMPANY BROCHURE: BEGIN")
        # print(company_brochure)
        # print("\nCOMPANY BROCHURE: END")
        print ("\n\nDone creating company brochure...\n")

        # SAVE OUTPUT AS MARKDOWN
        save_markdown(company_name, "English", company_brochure)
        
        ################################################################################
        # LANGUAGE TRANSLATION
        ################################################################################
        language_translation_prompts = LanguageTranslationPrompts(company_brochure, to_language=TARGET_LANGUAGE)
        llm = LargeLanguageModel(
            AI_MODEL, language_translation_prompts.system_prompt, language_translation_prompts.user_prompt)
        llm.stream_response()
        translated_company_brochure = llm.generate_text_response()
        save_markdown(company_name, TARGET_LANGUAGE, translated_company_brochure)
    except RuntimeError as e:
        print(f"❌ Error: {e}")

def save_markdown(company_name, language, brochure_text):
    print (f"\nWriting company brochure for {company_name} to file, written in {language}...\n")
    os.makedirs("./output", exist_ok=True)
    filename_base = company_name.replace(" ", "_").lower()
    filename_base = filename_base + '-' + language.lower()
    filepath = f"./output/{filename_base}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(brochure_text)
    print(f"✅ Markdown brochure saved to: {filepath}")
    print (f"\n Done writing company brochure for {company_name} to file, written in {language}...\n")

if __name__ == "__main__":
    main()
