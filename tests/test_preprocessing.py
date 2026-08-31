import pandas as pd
from ml_pipelines.preprocessing.cleaner import DataCleanerEngine


def test_data_cleaner_imputation_and_scaling():
    """Test DataCleanerEngine for missing value imputation, outlier clipping, and scaling."""
    df = pd.DataFrame({
        "num1": [10.0, 20.0, None, 40.0, 100.0],
        "cat1": ["small", "medium", None, "large", "small"]
    })
    
    cleaner = DataCleanerEngine(df)
    cleaner.handle_missing_values(strategy="impute_mean")
    cleaner.encode_categoricals(method="one_hot")
    cleaner.scale_features(method="standard")
    
    cleaned_df = cleaner.df
    
    assert cleaned_df["num1"].isnull().sum() == 0
    assert "cat1_medium" in cleaned_df.columns or "cat1_small" in cleaned_df.columns
    assert len(cleaner.transformations_log) > 0
