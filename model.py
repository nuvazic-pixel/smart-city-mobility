"""
Traffic Prediction Model — Linear Regression on hour + day_of_week features.

Kept intentionally simple for portfolio transparency.
Extension ideas:
  - RandomForestRegressor for non-linear patterns
  - Add weather features (temperature, rain)
  - Add public holiday flag
  - LSTM for sequence-aware forecasting
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


class TrafficPredictor:
    """
    Per-city linear regression model.
    Features: hour (int), day_of_week (int 0-6)
    Target:   traffic_volume (int, vehicles/hour)
    """

    def __init__(self):
        self.models: dict[str, LinearRegression] = {}
        self._is_fitted = False

    def fit(self, df: pd.DataFrame) -> "TrafficPredictor":
        """
        Train one model per city.

        Parameters
        ----------
        df : pd.DataFrame
            Must contain columns: city, hour, day_of_week, traffic_volume
        """
        for city, group in df.groupby("city"):
            X = group[["hour", "day_of_week"]].values
            y = group["traffic_volume"].values
            model = LinearRegression()
            model.fit(X, y)
            self.models[city] = model

        self._is_fitted = True
        return self

    def predict(self, city: str, hour: int, day_of_week: int) -> int:
        """
        Predict traffic volume for a city at a given hour and day.

        Parameters
        ----------
        city : str  — "Augsburg" or "Munich"
        hour : int  — 0–23
        day_of_week : int — 0 (Mon) … 6 (Sun)

        Returns
        -------
        int — predicted vehicles per hour (non-negative)
        """
        if not self._is_fitted:
            raise RuntimeError("Call .fit(df) before .predict().")
        if city not in self.models:
            raise ValueError(f"No model trained for city '{city}'.")

        pred = self.models[city].predict([[hour, day_of_week]])[0]
        return max(0, int(round(pred)))

    def evaluate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return MAE and R² per city on a held-out 20% test set.

        Returns
        -------
        pd.DataFrame with columns: city, MAE, R2
        """
        results = []
        for city, group in df.groupby("city"):
            X = group[["hour", "day_of_week"]].values
            y = group["traffic_volume"].values
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            model = LinearRegression()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            results.append(
                {
                    "city": city,
                    "MAE": round(mean_absolute_error(y_test, preds), 1),
                    "R2": round(r2_score(y_test, preds), 3),
                    "n_samples": len(group),
                }
            )
        return pd.DataFrame(results)
