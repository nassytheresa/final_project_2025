# app/etl/load.py
from app.database.mongo import get_db
from app.core.config import COLLECTION_NAME

def load_to_mongo(data):
    db = get_db()
    collection = db[COLLECTION_NAME]
    collection.insert_many(data)