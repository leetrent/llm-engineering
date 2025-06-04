class BrochureCreationPrompts:
    def __init__(self, company_name, website_content, brochure_links):
        self._set_system_prompt()
        self._set_user_prompt(company_name, website_content, brochure_links)

    def _set_system_prompt(self):
        self.system_prompt = (
            "You are an assistant that analyzes the contents of several relevant pages from a company website "
            "and creates a short brochure about the company for prospective customers, investors, and recruits. "
            "Respond in Markdown using proper formatting like #, **, -, and newlines. "
            "Include details of company culture, customers, and careers/jobs if you have the information."
        )

    def _set_user_prompt(self, company_name, website_content, brochure_links):
        self.user_prompt = f"You are looking at a company called: {company_name}\n"
        self.user_prompt += (
            "Here are the contents of its landing page and other relevant pages; "
            "use this information to build a short brochure of the company in markdown format.\n"
        )
        self.user_prompt += self._build_website_details(website_content, brochure_links)
        self.user_prompt = self.user_prompt[:5000]  # Truncate if more than 5,000 characters

    def _build_website_details(self, index_page_content, brochure_links):
        result = "Landing page:\n"
        result += index_page_content
        for link in brochure_links["links"]:
            result += f"\n\n{link['type']}\n"
            result += link.get("content", "[No content available]")
        return result
