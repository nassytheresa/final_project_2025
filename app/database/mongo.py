# app/database/mongo.py
from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import MONGODB_URI, DATABASE_NAME

def get_db() -> Database:
    """Get a mongo db connection to work with

    Returns:
        db: Database instance
    """
    client = MongoClient(MONGODB_URI)
    db: Database = client[DATABASE_NAME]
    return db
