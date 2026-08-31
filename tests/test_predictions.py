import numpy as np
import pandas as pd
from ml_pipelines.monitoring.drift_detector import DriftDetectorEngine


def test_drift_detection_psi_and_ks():
    """Test Population Stability Index (PSI) and Kolmogorov-Smirnov drift detection algorithms."""
    np.random.seed(42)
    reference = np.random.normal(0, 1, 1000)
    current_normal = np.random.normal(0, 1, 1000)
    current_drifted = np.random.normal(2, 1, 1000)
    
    psi_normal = DriftDetectorEngine.calculate_psi(reference, current_normal)
    psi_drifted = DriftDetectorEngine.calculate_psi(reference, current_drifted)
    
    assert psi_normal < 0.1  # Low/no drift
    assert psi_drifted > 0.2  # Significant drift detected
    
    detector = DriftDetectorEngine()
    ref_df = pd.DataFrame({"feat1": reference})
    curr_df = pd.DataFrame({"feat1": current_drifted})
    
    report = detector.analyze_dataset_drift(ref_df, curr_df)
    assert report["drift_detected"] is True
    assert "feat1" in report["feature_details"]
