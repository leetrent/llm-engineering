class LanguageTranslationPrompts:

    def __init__(self, content, to_language, from_language="English"):
        self.brochure_content = content
        self.source_language = from_language
        self.target_language = to_language
        self._set_system_prompt()
        self._set_user_prompt()

        print("\n")
        print(self.system_prompt)
        print("\n")
        print(self.user_prompt)
        print("\n")

    def _set_system_prompt(self):
        self.system_prompt = (
            "You are an interlingual translator who is capable of translating a document "
            "written in any language to any other language."
        )

    def _set_user_prompt(self):
        self.user_prompt = (
            f"As an interlingual translator, you have been provided with a company brochure "
            f"written in {self.source_language}. Please translate this company brochure to {self.target_language}. "
            f"Please keep the translated document in markdown format.\n\n"
            f"Here is the brochure content that needs to be translated:\n\n"
            f"```markdown\n{self.brochure_content}\n```"
        )
