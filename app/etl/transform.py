import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from app.ml.data_cleaner import CryptoDataCleanerModel
import os


def analyze_market_cap(df: pd.DataFrame) -> Dict:
    """
    Analyze market cap distribution and statistics.

    Args:
        df: DataFrame containing cryptocurrency data

    Returns:
        Dict containing market cap analysis results
    """
    market_cap_stats = {
        "total_market_cap": int(df["market_cap"].sum()),
        "top_10_market_cap": int(df.nlargest(10, "market_cap")["market_cap"].sum()),
        "market_cap_distribution": {
            "mean": float(df["market_cap"].mean()),
            "median": float(df["market_cap"].median()),
            "std": float(df["market_cap"].std()),
        },
    }
    return market_cap_stats


def analyze_price_changes(df: pd.DataFrame) -> Dict:
    """
    Analyze price changes and volatility.

    Args:
        df: DataFrame containing cryptocurrency data

    Returns:
        Dict containing price change analysis results
    """
    price_stats = {
        "avg_price_change_24h": float(df["price_change_percentage_24h"].mean()),
        "most_volatile": df.nlargest(5, "price_change_percentage_24h")[
            ["name", "price_change_percentage_24h"]
        ].to_dict("records"),
        "least_volatile": df.nsmallest(5, "price_change_percentage_24h")[
            ["name", "price_change_percentage_24h"]
        ].to_dict("records"),
    }
    return price_stats


def analyze_supply_metrics(df: pd.DataFrame) -> Dict:
    """
    Analyze supply metrics and utilization.

    Args:
        df: DataFrame containing cryptocurrency data

    Returns:
        Dict containing supply analysis results
    """
    # Calculate supply utilization
    df["supply_utilization"] = df["circulating_supply"] / df["total_supply"]

    supply_stats = {
        "avg_supply_utilization": float(df["supply_utilization"].mean()),
        "highest_utilization": df.nlargest(5, "supply_utilization")[
            ["name", "supply_utilization"]
        ].to_dict("records"),
        "lowest_utilization": df.nsmallest(5, "supply_utilization")[
            ["name", "supply_utilization"]
        ].to_dict("records"),
    }
    return supply_stats


def get_top_performers(df: pd.DataFrame) -> Dict:
    """
    Get top performing cryptocurrencies by various metrics.

    Args:
        df: DataFrame containing cryptocurrency data

    Returns:
        Dict containing top performers by different metrics
    """
    top_performers = {
        "by_market_cap": df.nlargest(10, "market_cap")[["name", "market_cap"]].to_dict(
            "records"
        ),
        "by_volume": df.nlargest(10, "total_volume")[["name", "total_volume"]].to_dict(
            "records"
        ),
        "by_price_change": df.nlargest(10, "price_change_percentage_24h")[
            ["name", "price_change_percentage_24h"]
        ].to_dict("records"),
    }
    return top_performers


def transform_data(df: pd.DataFrame) -> Dict:
    """
    Main transformation function that combines all analyses.

    Args:
        df: DataFrame containing cryptocurrency data

    Returns:
        Dict containing all analysis results
    """
    # Check if DataFrame is empty
    if df.empty:
        print("Warning: Empty DataFrame received")
        return {
            "market_cap_analysis": {
                "total_market_cap": 0,
                "top_10_market_cap": 0,
                "market_cap_distribution": {"mean": 0, "median": 0, "std": 0},
            },
            "price_analysis": {
                "avg_price_change_24h": 0,
                "most_volatile": [],
                "least_volatile": [],
            },
            "supply_analysis": {
                "avg_supply_utilization": 0,
                "highest_utilization": [],
                "lowest_utilization": [],
            },
            "top_performers": {
                "by_market_cap": [],
                "by_volume": [],
                "by_price_change": [],
            },
        }

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Initialize the data cleaner
    data_cleaner = CryptoDataCleanerModel(contamination=0.1)

    # Try to load existing model, if not available, train a new one
    model_path = "app/ml/models/data_cleaner.joblib"
    try:
        data_cleaner.load_model(model_path)
    except:
        print("Training new data cleaning model...")
        data_cleaner.fit(df)
        data_cleaner.save_model(model_path)

    # Clean the data using ML model
    cleaned_df, anomalous_df = data_cleaner.predict(df)

    # Log the number of anomalies detected
    print(
        f"Detected {len(anomalous_df)} anomalous data points out of {len(df)} total records"
    )

    # Remove duplicates based on id and timestamps
    cleaned_df = cleaned_df.drop_duplicates(subset=["id", "last_updated"], keep="last")

    # Handle remaining missing values
    cleaned_df["price_change_percentage_24h"] = cleaned_df[
        "price_change_percentage_24h"
    ].fillna(0)
    cleaned_df["market_cap"] = cleaned_df["market_cap"].fillna(0)
    cleaned_df["circulating_supply"] = cleaned_df["circulating_supply"].fillna(0)
    cleaned_df["total_supply"] = cleaned_df["total_supply"].fillna(
        cleaned_df["circulating_supply"]
    )

    # Remove rows with invalid data
    cleaned_df = cleaned_df[
        cleaned_df["market_cap"] > 0
    ]  # Remove coins with no market cap
    cleaned_df = cleaned_df[
        cleaned_df["current_price"] > 0
    ]  # Remove coins with no price

    # Convert numeric columns to appropriate types
    numeric_cols = [
        "current_price",
        "market_cap",
        "circulating_supply",
        "total_supply",
        "price_change_percentage_24h",
    ]
    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].apply(
        pd.to_numeric, errors="coerce"
    )

    # Calculate additional metrics
    cleaned_df["market_cap_rank"] = cleaned_df["market_cap"].rank(ascending=False)
    cleaned_df["price_volatility"] = cleaned_df["price_change_percentage_24h"].abs()

    return {
        "market_cap_analysis": analyze_market_cap(cleaned_df),
        "price_analysis": analyze_price_changes(cleaned_df),
        "supply_analysis": analyze_supply_metrics(cleaned_df),
        "top_performers": get_top_performers(cleaned_df),
    }
