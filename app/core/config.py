# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "crypto_data"
COLLECTION_NAME = "market_data"
