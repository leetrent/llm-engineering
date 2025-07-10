import os
from dotenv import load_dotenv

def retrieve_api_key_value(api_key):
    load_dotenv(override=True)
    api_key_value = os.getenv(api_key)
    if not api_key_value:
        raise RuntimeError(f"❌ No API key value found in .env for '{api_key}'.")
    return api_key_value