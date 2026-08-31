from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats


class DriftDetectorEngine:
    """Drift Detection Engine for Population Stability Index (PSI) & Kolmogorov-Smirnov (KS) testing."""

    @staticmethod
    def calculate_psi(reference: np.ndarray, current: np.ndarray, num_bins: int = 10) -> float:
        """Compute Population Stability Index (PSI) between baseline reference and current dataset."""
        reference = reference[~np.isnan(reference)]
        current = current[~np.isnan(current)]

        if len(reference) == 0 or len(current) == 0:
            return 0.0

        percentiles = np.linspace(0, 100, num_bins + 1)
        bins = np.percentile(reference, percentiles)
        bins[0] = -np.inf
        bins[-1] = np.inf

        ref_counts, _ = np.histogram(reference, bins=bins)
        curr_counts, _ = np.histogram(current, bins=bins)

        ref_pct = ref_counts / len(reference)
        curr_pct = curr_counts / len(current)

        # Smooth zero counts to avoid log(0)
        ref_pct = np.where(ref_pct == 0, 0.0001, ref_pct)
        curr_pct = np.where(curr_pct == 0, 0.0001, curr_pct)

        psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
        return float(psi)

    @staticmethod
    def calculate_ks_test(reference: np.ndarray, current: np.ndarray) -> Tuple[float, float]:
        """Perform two-sample Kolmogorov-Smirnov test for goodness of fit."""
        res = stats.ks_2samp(reference, current)
        return float(res.statistic), float(res.pvalue)

    def analyze_dataset_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame) -> Dict[str, Any]:
        """Examine feature-level drift across all numeric columns."""
        feature_results = {}
        total_psi = []
        drift_flag = False

        common_cols = [c for c in reference_df.select_dtypes(include=[np.number]).columns if c in current_df.columns]

        for col in common_cols:
            ref_vals = reference_df[col].dropna().values
            curr_vals = current_df[col].dropna().values

            if len(ref_vals) == 0 or len(curr_vals) == 0:
                continue

            psi_score = self.calculate_psi(ref_vals, curr_vals)
            ks_stat, p_val = self.calculate_ks_test(ref_vals, curr_vals)
            total_psi.append(psi_score)

            is_feature_drift = psi_score > 0.2 or p_val < 0.05
            if is_feature_drift:
                drift_flag = True

            feature_results[col] = {
                "psi_score": round(psi_score, 4),
                "ks_statistic": round(ks_stat, 4),
                "p_value": round(p_val, 4),
                "drift_detected": is_feature_drift
            }

        avg_psi = float(np.mean(total_psi)) if total_psi else 0.0

        return {
            "overall_drift_score": round(avg_psi, 4),
            "drift_detected": drift_flag,
            "feature_details": feature_results,
            "samples_analyzed": len(current_df)
        }
