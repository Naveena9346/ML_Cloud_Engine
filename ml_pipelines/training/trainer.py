from typing import Any, Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor


class ModelTrainerEngine:
    """Universal Machine Learning Trainer Engine supporting Scikit-learn, XGBoost, and LightGBM."""

    def __init__(self, df: pd.DataFrame, target_column: str, model_type: str = "CLASSIFICATION"):
        self.df = df
        self.target_column = target_column
        self.model_type = model_type.upper()
        
        self.X = self.df.drop(columns=[target_column])
        self.y = self.df[target_column]

    def split_data(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Split features and target into training and evaluation sets."""
        return train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)

    def get_model(self, algorithm: str, params: Dict[str, Any] = None):
        """Instantiate target model with specified hyperparameters."""
        params = params or {}
        algo = algorithm.upper()

        if self.model_type == "CLASSIFICATION":
            if algo == "RANDOM_FOREST":
                return RandomForestClassifier(**params)
            elif algo == "XGBOOST":
                return XGBClassifier(**params, eval_metric="logloss")
            elif algo == "LIGHTGBM":
                return LGBMClassifier(**params, verbose=-1)
            elif algo == "GRADIENT_BOOSTING":
                return GradientBoostingClassifier(**params)
            elif algo == "LOGISTIC_REGRESSION":
                return LogisticRegression(**params, max_iter=1000)
            else:
                return RandomForestClassifier(**params)
        else:
            if algo == "RANDOM_FOREST":
                return RandomForestRegressor(**params)
            elif algo == "XGBOOST":
                return XGBRegressor(**params)
            elif algo == "LIGHTGBM":
                return LGBMRegressor(**params, verbose=-1)
            elif algo == "GRADIENT_BOOSTING":
                return GradientBoostingRegressor(**params)
            elif algo == "LINEAR_REGRESSION":
                return LinearRegression(**params)
            else:
                return RandomForestRegressor(**params)

    def train(self, algorithm: str, params: Dict[str, Any] = None) -> Tuple[Any, Dict[str, Any], pd.DataFrame, pd.Series]:
        """Train the model and return the model instance, evaluation predictions, and signature."""
        X_train, X_test, y_train, y_test = self.split_data()
        model = self.get_model(algorithm, params)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        y_proba = None
        if self.model_type == "CLASSIFICATION" and hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)

        results = {
            "y_test": y_test,
            "y_pred": y_pred,
            "y_proba": y_proba,
            "X_test": X_test
        }
        
        return model, results, X_train, y_train
