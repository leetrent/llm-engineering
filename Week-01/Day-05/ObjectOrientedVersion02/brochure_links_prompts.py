import textwrap

class BrochureLinksPrompts:
    def __init__(self, url, website_links):
        self._set_system_prompt()
        self._set_user_prompt(url, website_links)

    def _set_system_prompt(self):
        self.system_prompt = (
            "You are provided with a list of links found on a webpage. "
            "You are able to decide which of the links would be most relevant to include in a brochure about the company, "
            "such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
            "You should respond in JSON as in this example:\n"
            + textwrap.dedent("""\
                {
                    "links": [
                        {"type": "about page", "url": "https://full.url/goes/here/about"},
                        {"type": "careers page", "url": "https://another.full.url/careers"}
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
