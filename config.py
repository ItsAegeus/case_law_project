import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COURTLISTENER_API_URL = "https://www.courtlistener.com/api/rest/v3/search/"