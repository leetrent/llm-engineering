import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

# Remove IPython.display — it doesn't apply outside of notebooks
# from IPython.display import Markdown, display

# Use regular print() instead
def print_markdown(text):
    print(text)  # You could add fancier Markdown formatting later

# Optional test to confirm it works
if __name__ == "__main__":
    print_markdown("✅ Your imports ran successfully!")
