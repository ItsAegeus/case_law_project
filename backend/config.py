import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COURTLISTENER_API_KEY = os.getenv("COURTLISTENER_API_KEY")
