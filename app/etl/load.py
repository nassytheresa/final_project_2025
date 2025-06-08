import json
from datetime import datetime, timezone
from typing import Dict
import pandas as pd
from pathlib import Path
import numpy as np
from app.storage.mongo import get_db
from app.core.config import COLLECTION_NAME


def convert_numpy_types(obj):
    """Convert NumPy types to Python native types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj


def save_analysis_results(
    analysis_results: Dict, collection_name: str = "analysis_results"
):
    """
    Save analysis results to MongoDB.

    Args:
        analysis_results: Dictionary containing analysis results
        collection_name: Name of the MongoDB collection to save results to
    """
    db = get_db()
    collection = db[collection_name]

    # Add timestamp to the results
    analysis_results["timestamp"] = datetime.now(timezone.utc)

    # Convert NumPy types to Python native types
    analysis_results = convert_numpy_types(analysis_results)

    # Insert the results
    collection.insert_one(analysis_results)


def save_to_csv(df: pd.DataFrame, filename: str):
    """
    Save DataFrame to CSV file.

    Args:
        df: DataFrame to save
        filename: Name of the CSV file
    """
    df.to_csv(filename, index=False)


def export_analysis_to_json(analysis_results: Dict, filename: str):
    """
    Export analysis results to JSON file.

    Args:
        analysis_results: Dictionary containing analysis results
        filename: Name of the JSON file
    """
    # Convert NumPy types to Python native types
    analysis_results = convert_numpy_types(analysis_results)

    # Add timestamp
    analysis_results["timestamp"] = datetime.now(timezone.utc).isoformat()

    # Create output directory if it doesn't exist
    output_dir = Path(filename).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save to JSON file
    with open(filename, "w") as f:
        json.dump(analysis_results, f, indent=2)
