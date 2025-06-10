import sys
from brochure_creation_helpers import process_website_links
from brochure_creation_helpers import process_brochure_links
from brochure_creation_helpers import process_brochure_creation
from brochure_creation_helpers import process_language_translation
from brochure_creation_helpers import write_markdown_to_file
from brochure_creation_helpers import clean_translated_output
   
def main():
    AI_MODEL = "gpt-4o-mini"
   
    if len(sys.argv) < 3:
        print("Usage: python brochure_creation_main.py <URL> <COMPANY_NAME><TARGET LANGUAGE>")
        sys.exit(1)

    url = sys.argv[1]
    company_name = sys.argv[2]
    target_language = sys.argv[3]

    try:
        ################################################################################
        # WEBSITE LINKS
        ################################################################################
        website_links, website_content = process_website_links(url)

        ################################################################################
        # BROCHURE LINKS
        ################################################################################
        brochure_links = process_brochure_links(url, website_links, AI_MODEL)
        
        ################################################################################
        # BROCHURE CREATION
        ################################################################################      
        company_brochure = process_brochure_creation(company_name, website_content, brochure_links, AI_MODEL)
        cleaned_company_brochure = clean_translated_output(company_brochure)

        ################################################################################
        # SAVE BROCHURE WRITTEN IN ENGLISH AS MARKDOWN
        ################################################################################
        write_markdown_to_file(company_name, "English", cleaned_company_brochure)
        
        ################################################################################
        # LANGUAGE TRANSLATION
        ################################################################################
        translated_company_brochure = process_language_translation(company_brochure, target_language, AI_MODEL)
        cleaned_translated_company_brochure = clean_translated_output(translated_company_brochure)
        
        ################################################################################
        # SAVE BROCHURE WRITTEN IN THE TARGET  AS MARKDOWN
        ################################################################################
        write_markdown_to_file(company_name, target_language, cleaned_translated_company_brochure)
        
    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
