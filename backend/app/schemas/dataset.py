from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DatasetBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    data_type: str = "TABULAR"
    file_format: str = "CSV"


class DatasetCreate(DatasetBase):
    project_id: str


class DataCleaningOptions(BaseModel):
    missing_value_strategy: str = "impute_mean"  # impute_mean, impute_median, impute_mode, drop
    outlier_handling: str = "iqr_clip"           # iqr_clip, zscore_clip, none
    categorical_encoding: str = "one_hot"        # one_hot, ordinal, none
    scaling: str = "standard"                    # standard, minmax, none
    columns_to_drop: Optional[List[str]] = None


class DatasetVersionResponse(BaseModel):
    id: str
    dataset_id: str
    version_number: int
    file_path: str
    file_size_bytes: int
    row_count: int
    column_count: int
    sha256_checksum: Optional[str] = None
    schema_json: Optional[Dict[str, Any]] = None
    eda_summary: Optional[Dict[str, Any]] = None
    cleaned_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FeatureStoreItem(BaseModel):
    id: str
    dataset_version_id: str
    feature_name: str
    feature_type: str
    transformation_rules: Optional[Dict[str, Any]] = None
    sample_values: Optional[List[Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DatasetResponse(DatasetBase):
    id: str
    project_id: str
    current_version: int
    created_at: datetime
    updated_at: datetime
    latest_version: Optional[DatasetVersionResponse] = None

    class Config:
        from_attributes = True
