from website_details import WebsiteDetails

class BrochureCreationPrompts:
    def __init__(self,company_name, website_content, brochure_links):
        self._set_system_prompt()
        self._set_user_prompt(company_name, website_content, brochure_links)
        
    def _set_system_prompt(self):
        self.system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."
    
    def _set_user_prompt(self, company_name, website_content, brochure_links):
        self.user_prompt = f"You are looking at a company called: {company_name}\n"
        self.user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        self.user_prompt += self._build_website_details(website_content, brochure_links)
        self.user_prompt = self.user_prompt[:5_000] # Truncate if more than 5,000 characters
    
    def _build_website_details(self, website_content, brochure_links):
        result = "Landing page:\n"
        result += website_content
        for link in brochure_links["links"]:
            result += f"\n\n{link['type']}\n"
            result += WebsiteDetails(link["url"]).content
        return result