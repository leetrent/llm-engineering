import os
from dotenv import load_dotenv

def get_brochure_links_from_website_links(url, website_links):
    # URL
    print("\nurl", url)
    
    # WEBSITE LINKS
    print("\nwebsite_links: BEGIN")
    print(website_links)
    print("website_links: END")
    
    # API KEY
    api_key = get_api_key()
    print("\napi_key", api_key)
    
    # SYSTEM PROMPT
    system_prompt = get_system_prompt()
    print("\nsystem_prompt: BEGIN")
    print(system_prompt)
    print("system_prompt: END")
    
   # USER PROMPT
    user_prompt = get_user_prompt(url, website_links)
    print("\nuser_prompt: BEGIN")
    print(user_prompt)
    print("user_prompt: END")
          
    # RETURN BROCHURE LINKS
    return website_links
    
def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found in .env.")
    return api_key
    
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