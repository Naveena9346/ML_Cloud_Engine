from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler


class DataCleanerEngine:
    """Enterprise-grade data cleaning, outlier detection, imputation, and encoding engine."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.transformations_log: List[str] = []

    def handle_missing_values(self, strategy: str = "impute_mean") -> "DataCleanerEngine":
        """Handle null/missing values across numerical and categorical columns."""
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        cat_cols = self.df.select_dtypes(include=["object", "category", "string"]).columns

        if strategy == "impute_mean":
            for col in num_cols:
                if self.df[col].isnull().sum() > 0:
                    mean_val = self.df[col].mean()
                    self.df[col] = self.df[col].fillna(mean_val)
                    self.transformations_log.append(f"Imputed missing in '{col}' with mean ({mean_val:.4f})")
            for col in cat_cols:
                if self.df[col].isnull().sum() > 0:
                    mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else "UNKNOWN"
                    self.df[col] = self.df[col].fillna(mode_val)
                    self.transformations_log.append(f"Imputed missing in categorical '{col}' with mode ('{mode_val}')")

        elif strategy == "impute_median":
            for col in num_cols:
                if self.df[col].isnull().sum() > 0:
                    median_val = self.df[col].median()
                    self.df[col] = self.df[col].fillna(median_val)
                    self.transformations_log.append(f"Imputed missing in '{col}' with median ({median_val:.4f})")
            for col in cat_cols:
                if self.df[col].isnull().sum() > 0:
                    mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else "UNKNOWN"
                    self.df[col] = self.df[col].fillna(mode_val)

        elif strategy == "drop":
            before_cnt = len(self.df)
            self.df = self.df.dropna()
            after_cnt = len(self.df)
            self.transformations_log.append(f"Dropped {before_cnt - after_cnt} rows with null values")

        return self

    def handle_outliers(self, method: str = "iqr_clip", factor: float = 1.5) -> "DataCleanerEngine":
        """Identify and clip numerical outliers using IQR or Z-Score bounds."""
        if method == "none":
            return self

        num_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if method == "iqr_clip":
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - (factor * iqr)
                upper_bound = q3 + (factor * iqr)
                
                outliers_cnt = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
                if outliers_cnt > 0:
                    self.df[col] = np.clip(self.df[col], lower_bound, upper_bound)
                    self.transformations_log.append(f"Clipped {outliers_cnt} outliers in '{col}' via IQR bounds [{lower_bound:.2f}, {upper_bound:.2f}]")

            elif method == "zscore_clip":
                std = self.df[col].std()
                mean = self.df[col].mean()
                if std > 0:
                    lower_bound = mean - (factor * std)
                    upper_bound = mean + (factor * std)
                    self.df[col] = np.clip(self.df[col], lower_bound, upper_bound)
                    self.transformations_log.append(f"Clipped outliers in '{col}' via Z-score bounds")

        return self

    def encode_categoricals(self, method: str = "one_hot") -> "DataCleanerEngine":
        """Convert categorical features to numeric representations."""
        if method == "none":
            return self

        cat_cols = self.df.select_dtypes(include=["object", "category", "string"]).columns
        if len(cat_cols) == 0:
            return self

        if method == "one_hot":
            self.df = pd.get_dummies(self.df, columns=list(cat_cols), drop_first=True, dtype=float)
            self.transformations_log.append(f"Applied One-Hot Encoding on columns: {list(cat_cols)}")
        elif method == "ordinal":
            for col in cat_cols:
                self.df[col] = self.df[col].astype("category").cat.codes.astype(float)
                self.transformations_log.append(f"Applied Ordinal Encoding on column: '{col}'")

        return self

    def scale_features(self, method: str = "standard", exclude_cols: List[str] = None) -> "DataCleanerEngine":
        """Scale numerical features using Standard, MinMax, or Robust Scalers."""
        if method == "none":
            return self

        exclude_cols = exclude_cols or []
        num_cols = [c for c in self.df.select_dtypes(include=[np.number]).columns if c not in exclude_cols]

        if len(num_cols) == 0:
            return self

        if method == "standard":
            scaler = StandardScaler()
        elif method == "minmax":
            scaler = MinMaxScaler()
        elif method == "robust":
            scaler = RobustScaler()
        else:
            return self

        self.df[num_cols] = scaler.fit_transform(self.df[num_cols])
        self.transformations_log.append(f"Applied {method.capitalize()} Scaler to {len(num_cols)} numerical features")
        return self

    def execute_pipeline(self, options: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """Run the complete automated data cleaning sequence."""
        self.handle_missing_values(strategy=options.get("missing_value_strategy", "impute_mean"))
        self.handle_outliers(method=options.get("outlier_handling", "iqr_clip"))
        self.encode_categoricals(method=options.get("categorical_encoding", "one_hot"))
        self.scale_features(method=options.get("scaling", "standard"), exclude_cols=options.get("exclude_cols", []))
        return self.df, self.transformations_log
