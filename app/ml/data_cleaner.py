import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, List
import joblib
import os


class CryptoDataCleanerModel:
    def __init__(self, contamination: float = 0.1):
        """
        Initialize the data cleaner with an Isolation Forest model.

        Args:
            contamination: The proportion of outliers in the data set (default: 0.1)
        """
        self.model = IsolationForest(
            contamination=contamination, random_state=42, n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for the model by selecting relevant columns and scaling.

        Args:
            df: Input DataFrame

        Returns:
            Scaled features array
        """
        # Select relevant features for anomaly detection
        features = [
            "current_price",
            "market_cap",
            "circulating_supply",
            "total_supply",
            "price_change_percentage_24h",
        ]

        # Handle missing values
        X = df[features].fillna(0)

        # Scale the features
        if not self.is_fitted:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)

        return X_scaled

    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit the anomaly detection model on the data.

        Args:
            df: Training DataFrame
        """
        X = self._prepare_features(df)
        self.model.fit(X)
        self.is_fitted = True

    def predict(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Predict anomalies in the data and return cleaned and anomalous data separately.

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (cleaned_data, anomalous_data)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")

        X = self._prepare_features(df)
        predictions = self.model.predict(X)

        # Split data into normal and anomalous
        normal_mask = predictions == 1
        anomalous_mask = predictions == -1

        cleaned_data = df[normal_mask].copy()
        anomalous_data = df[anomalous_mask].copy()

        return cleaned_data, anomalous_data

    def save_model(self, path: str = "app/ml/models/data_cleaner.joblib") -> None:
        """
        Save the fitted model and scaler to disk.

        Args:
            path: Path to save the model
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({"model": self.model, "scaler": self.scaler}, path)

    def load_model(self, path: str = "app/ml/models/data_cleaner.joblib") -> None:
        """
        Load a fitted model and scaler from disk.

        Args:
            path: Path to the saved model
        """
        saved_data = joblib.load(path)
        self.model = saved_data["model"]
        self.scaler = saved_data["scaler"]
        self.is_fitted = True
