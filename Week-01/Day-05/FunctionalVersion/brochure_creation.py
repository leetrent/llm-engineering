import os
from dotenv import load_dotenv
from openai import OpenAI
import json

def create_brochure(company_name, url,  brochuree_links):
    # COMPANY NAME
    print("\company_name", company_name)
    
    # URL
    print("\nurl", url)
    
    # BROCHURE LINKS
    print("\brochuree_links: BEGIN")
    print(brochuree_links)
    print("brochuree_links: END")
    
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
          
    # BROCHURE LINKS
    brochure_links = get_brochure_links(api_key, system_prompt, user_prompt)
    print("\nbrochure_links: BEGIN")
    print(brochure_links)
    print("brochure_links: END")
    
    # RETURN BROCHURE LINKS
    return brochure_links
    
def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found in .env.")
    return api_key
    
def get_system_prompt():
    system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."
    return system_prompt

def get_user_prompt(url, website_links):
    user_prompt = f"Here is the list of links on the website of {url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website_links)
    return user_prompt

def get_brochure_links(api_key, system_prompt, user_prompt):
    openai_client = OpenAI(api_key=api_key)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    
    print("\nJSON RESULT", result)
    return json.loads(result)