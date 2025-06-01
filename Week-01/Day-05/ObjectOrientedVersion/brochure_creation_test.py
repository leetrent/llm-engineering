import sys
from website import Website
from large_language_model import LargeLanguageModel

def main():
    if len(sys.argv) < 3:
        print("Usage: expcted two arguments <URL>, <COMPANY_NAME>")
        sys.exit(1)

    url = sys.argv[1]
    company_name = sys.argv[2]
    
    try:
        # WEBSITE LINKS
        website = Website(url)
        website._fetch_and_parse()
        
        print("\nWEBSITE LINKS: BEGIN")
        for link in website.links:
            print(link)
        print("WEBSITE LINKS: END")
        
        # BROCHURE LINKS
        system_prompt = get_system_prompt_for_brochure_links()
        user_prompt = get_user_prompt_for_brochure_links(website.url, website.links)
        brochure_links = LargeLanguageModel("gpt-4o-mini", system_prompt, user_prompt)._create_completions_in_json()
        
        print("\nBROCHURE LINKS: BEGIN")
        print(brochure_links)
        print("BROCHURE LINKS: END")
        
        system_prompt = get_system_prompt_for_brochure_creation()
        user_prompt = get_user_prompt_for_brochure_creation(company_name, website.content, brochure_links)
        company_brochure = LargeLanguageModel("gpt-4o-mini", system_prompt, user_prompt)._create_completions()
        print("\nCOMPANY BROCHURE: BEGIN")
        print(company_brochure)
        print("\nCOMPANY BROCHURE: END")
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        
def get_system_prompt_for_brochure_links():
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

def get_user_prompt_for_brochure_links(url, website_links):
    user_prompt = f"Here is the list of links on the website of {url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website_links)
    return user_prompt

def get_all_details(website_content, brochure_links):
    result = "Landing page:\n"
    result += website_content
    for link in brochure_links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).content
    return result


def get_system_prompt_for_brochure_creation():
    return "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."


def get_user_prompt_for_brochure_creation(company_name, website_content, brochure_links):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(website_content, brochure_links)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

if __name__ == "__main__":
    main()
