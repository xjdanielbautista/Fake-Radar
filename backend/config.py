# config.py
# Application configuration and python environment variables

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"