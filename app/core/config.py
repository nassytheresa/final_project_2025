# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://tempress-mongo:27017/")
DATABASE_NAME = "crypto_db"
COLLECTION_NAME = "market_data"

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
