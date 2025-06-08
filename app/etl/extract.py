from typing import List, Dict
import pandas as pd
from datetime import datetime, timedelta, timezone
from app.storage.mongo import get_db
from app.core.config import COLLECTION_NAME


def extract_crypto_data(days: int = 1) -> pd.DataFrame:
    """
    Extract cryptocurrency data from MongoDB.

    Args:
        days: Number of days of historical data to extract

    Returns:
        DataFrame containing cryptocurrency data
    """
    # Get MongoDB collection
    collection = get_db()[COLLECTION_NAME]

    # Calculate date threshold as string in ISO format
    date_threshold = (datetime.now(timezone.utc) - timedelta(days=days)).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    try:
        # Query the data with date filter
        cursor = collection.find(
            {
                "$or": [
                    {"last_updated": {"$gte": date_threshold}},
                    {
                        "last_updated": {"$exists": False}
                    },  # Include documents without last_updated
                ]
            }
        )
        data = list(cursor)

        # If no data found with date filter, get all data
        if not data:
            print("No data found with date filter, fetching all available data...")
            cursor = collection.find()
            data = list(cursor)

        print(f"Found {len(data)} records")

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Convert timestamp columns to datetime
        if "last_updated" in df.columns:
            df["last_updated"] = pd.to_datetime(df["last_updated"])

        # Ensure required columns exist
        required_columns = [
            "id",
            "name",
            "current_price",
            "market_cap",
            "circulating_supply",
            "total_supply",
            "price_change_percentage_24h",
            "last_updated",
        ]

        # Add missing columns with default values
        for col in required_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found, adding with default values")
                if col == "price_change_percentage_24h":
                    df[col] = 0.0
                elif col in ["market_cap", "circulating_supply", "total_supply"]:
                    df[col] = 0.0
                elif col == "current_price":
                    df[col] = 0.0
                else:
                    df[col] = None
        df["price"] = df["current_price"]
        return df

    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error
