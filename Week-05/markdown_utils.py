import re

def clean_translated_output(raw_output):
    """
    Removes surrounding triple backticks and 'markdown' from LLM output, if present.
    Ensures proper markdown rendering in editors like VS Code.
    """
    return re.sub(r'^```markdown\n(.*?)\n```$', r'\1', raw_output.strip(), flags=re.DOTALL)
