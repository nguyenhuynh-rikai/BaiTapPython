import os
from dotenv import load_dotenv

# load file .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DEBUG = os.getenv("DEBUG")

