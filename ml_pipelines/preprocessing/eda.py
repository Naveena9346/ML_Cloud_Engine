from typing import Any, Dict, List
import numpy as np
import pandas as pd


class EDAEngine:
    """Automated Exploratory Data Analysis & Statistical Profiling Engine."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate_summary(self) -> Dict[str, Any]:
        """Compute dataset overview metrics, schema, and null value analysis."""
        total_rows, total_cols = self.df.shape
        missing_cells = int(self.df.isnull().sum().sum())
        total_cells = total_rows * total_cols
        missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0.0

        schema: List[Dict[str, Any]] = []
        column_summaries: Dict[str, Any] = {}

        for col in self.df.columns:
            dtype_str = str(self.df[col].dtype)
            null_cnt = int(self.df[col].isnull().sum())
            null_pct = float(null_cnt / total_rows * 100) if total_rows > 0 else 0.0
            unique_cnt = int(self.df[col].nunique())

            col_info = {
                "name": col,
                "type": dtype_str,
                "null_count": null_cnt,
                "null_pct": round(null_pct, 2),
                "unique_count": unique_cnt,
            }
            schema.append(col_info)

            # Numerical statistics
            if pd.api.types.is_numeric_dtype(self.df[col]):
                column_summaries[col] = {
                    "mean": float(self.df[col].mean()) if not self.df[col].isnull().all() else None,
                    "std": float(self.df[col].std()) if not self.df[col].isnull().all() else None,
                    "min": float(self.df[col].min()) if not self.df[col].isnull().all() else None,
                    "q25": float(self.df[col].quantile(0.25)) if not self.df[col].isnull().all() else None,
                    "median": float(self.df[col].median()) if not self.df[col].isnull().all() else None,
                    "q75": float(self.df[col].quantile(0.75)) if not self.df[col].isnull().all() else None,
                    "max": float(self.df[col].max()) if not self.df[col].isnull().all() else None,
                    "skewness": float(self.df[col].skew()) if not self.df[col].isnull().all() else None,
                }
            else:
                top_counts = self.df[col].value_counts().head(5).to_dict()
                column_summaries[col] = {
                    "top_categories": {str(k): int(v) for k, v in top_counts.items()}
                }

        # Correlation Matrix for numerical columns
        num_df = self.df.select_dtypes(include=[np.number])
        correlation_matrix = {}
        if num_df.shape[1] > 1:
            corr = num_df.corr().round(4)
            correlation_matrix = {
                "columns": list(corr.columns),
                "values": corr.values.tolist()
            }

        return {
            "overview": {
                "total_rows": total_rows,
                "total_columns": total_cols,
                "missing_cells": missing_cells,
                "missing_percentage": round(missing_percentage, 2),
                "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 3)
            },
            "schema": schema,
            "column_summaries": column_summaries,
            "correlation_matrix": correlation_matrix,
        }
