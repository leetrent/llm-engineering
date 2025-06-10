import os
import re
from website_details import WebsiteDetails
from brochure_links_prompts import BrochureLinksPrompts
from brochure_creation_prompts import BrochureCreationPrompts
from large_language_model import LargeLanguageModel
from language_translation_prompts import LanguageTranslationPrompts

################################################################################
# WEBSITE LINKS
################################################################################
def get_website_links(url):
    website = WebsiteDetails(url)
    website.fetch()    
    return website

def print_website_links(website_links):
        print("\nWEBSITE LINKS: BEGIN")
        for link in website_links:
            print(link)
        print("WEBSITE LINKS: END")

def process_website_links(url):
    website = get_website_links(url)
    print_website_links(website.links)
    return website.links, website.content

################################################################################
# BROCHURE LINKS
################################################################################
def get_brochure_links(url, website_links, ai_model):
    brochure_links_prompts = BrochureLinksPrompts(url, website_links)
    llm = LargeLanguageModel(
        ai_model, brochure_links_prompts.system_prompt, brochure_links_prompts.user_prompt
    )
    return llm.generate_json_response()

def enrich_brochure_links(brochure_links):
    for link in brochure_links["links"]:
        try:
            enriched = WebsiteDetails(link["url"])
            enriched.fetch()
            link["content"] = enriched.content
        except Exception as e:
            link["content"] = "[Error fetching content]"    
    return brochure_links
    
def print_brochure_links(brochure_links):
    print("\nBROCHURE LINKS: BEGIN")
    # print(brochure_links)
    # print("\n")
    for link in brochure_links["links"]:
        print(link["type"], ' - ', link["url"])
    print("\n")
    print("BROCHURE LINKS: END")
       
def process_brochure_links(url, website_links, ai_model):
    brochure_links = get_brochure_links(url, website_links, ai_model)
    enriched_brochure_links = enrich_brochure_links(brochure_links)
    print_brochure_links(enriched_brochure_links)
    return enriched_brochure_links

################################################################################
# BROCHURE CREATION
################################################################################
def process_brochure_creation(company_name, website_content, brochure_links, ai_model):
        brochure_creation_prompts = BrochureCreationPrompts(
            company_name, website_content, brochure_links
        )

        llm = LargeLanguageModel(
            ai_model, brochure_creation_prompts.system_prompt, brochure_creation_prompts.user_prompt)
        llm.stream_response()
        
        return llm.generate_text_response()

################################################################################
# LANGUAGE TRANSLATION
################################################################################
def process_language_translation(company_brochure, target_language, ai_model):
    language_translation_prompts = LanguageTranslationPrompts(company_brochure, target_language)
    llm = LargeLanguageModel(
        ai_model, language_translation_prompts.system_prompt, language_translation_prompts.user_prompt)
    llm.stream_response()
    return llm.generate_text_response()
    

################################################################################
# WRITE MARKDOWN TO FILE
################################################################################
def write_markdown_to_file(company_name, language, brochure_text):
    print (f"\nWriting company brochure for {company_name} to file, written in {language}...\n")
    os.makedirs("./output", exist_ok=True)
    filename_base = company_name.replace(" ", "_").lower()
    filename_base = filename_base + '-' + language.lower()
    filepath = f"./output/{filename_base}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(brochure_text)
    print(f"✅ Markdown brochure saved to: {filepath}")
    print (f"\n Done writing company brochure for {company_name} to file, written in {language}...\n")
    
################################################################################
# CLEAN TRANSLATED OUTPUT
################################################################################  
def clean_translated_output(raw_output):
    """
    Removes surrounding triple backticks and 'markdown' from LLM output, if present.
    Ensures proper markdown rendering in editors like VS Code.
    """
    return re.sub(r'^```markdown\n(.*?)\n```$', r'\1', raw_output.strip(), flags=re.DOTALL)
