class BrochureCreationPrompts:
    def __init__(self, company_name, website_content):
        self._set_system_prompt()
        self._set_user_prompt(company_name, website_content)

    def _set_system_prompt(self):
        self.system_prompt = (
            "You are an assistant that analyzes the contents of a company's website landing page " \
            "and creates a brochure about the company for prospective customers, investors and recruits. "
            " Respond in markdown."
        )

    def _set_user_prompt(self, company_name, website_content):
        self.user_prompt = f"Please generate a company brocure for {company_name}.\n"
        self.user_prompt += "Here are the contents of company's landing page:\n"
        self.user_prompt += website_content
        self.user_prompt = self.user_prompt[:5000]  # Truncate if more than 5,000 characters
