import textwrap

class BrochureLinksPrompts:
    def __init__(self, url, website_links):
        self._set_system_prompt()
        self._set_user_prompt(url, website_links)

    def _set_system_prompt(self):
        self.system_prompt = (
            "You are provided with a list of links found on a webpage. "
            "You are able to decide which of the links would be most relevant to include in a brochure about the company, "
            "such as links to the company or index page. "
            "Please also add an 'About' section to this brochure if there is an 'about' or'about us' page. "
            "Pleaee also add a 'Contact Us' section to this brochure if there is a 'contact' or 'contact us' page. "
            "Please also add a 'Careers' section to this brochure if there is a 'careers' or 'jobs' page. "
            "Please also add a section or sections to this brochure for topics not already discussed here "
            "that you deem relevant to the creation of a company brochure.\n"
            "Your response using one array of JSON object in the format specified below is mandatory. "
            "The brochure content and the number of sections in this brochure will vary depending on the links that have been provided to you."
            "Please respond with one array of JSON objects using this format:\n"
            + textwrap.dedent("""\
                {
                    "links": [
                        {"type": "about page", "url": "https://<domain name>/"},
                        {"type": "about page", "url": "https://<domain name>/about"},
                        {"type": "careers page", "url": "https://<domain name>/careers"}
                    ]
                }
            """)

        )

    def _set_user_prompt(self, url, website_links):
        self.user_prompt = (
            f"Here is the list of links on the website of {url} - "
            "please decide which of these are relevant web links for a brochure about the company. "
            "Respond with the full https URL in JSON format. Do not include Terms of Service, Privacy, or email links.\n"
            "Links (some might be relative links):\n"
            + "\n".join(website_links)
        )
