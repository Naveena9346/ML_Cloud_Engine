from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TrainingJobCreate(BaseModel):
    project_id: str
    dataset_version_id: str
    name: str = Field(..., min_length=2, max_length=255)
    algorithm: str = "XGBOOST"  # RANDOM_FOREST, XGBOOST, LIGHTGBM, PYTORCH_NN, LOGISTIC_REGRESSION
    target_column: str
    model_type: str = "CLASSIFICATION"  # CLASSIFICATION, REGRESSION
    hyperparameters: Optional[Dict[str, Any]] = None
    enable_tuning: bool = False
    tuning_trials: int = 10


class ExperimentRunResponse(BaseModel):
    id: str
    training_job_id: str
    run_name: str
    run_number: int
    status: str
    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    artifacts: Optional[Dict[str, Any]] = None
    epoch_logs: Optional[List[Dict[str, Any]]] = None
    duration_seconds: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TrainingJobResponse(BaseModel):
    id: str
    project_id: str
    dataset_version_id: str
    name: str
    algorithm: str
    target_column: str
    model_type: str
    status: str
    hyperparameters: Optional[Dict[str, Any]] = None
    hyperparameter_tuning: Optional[Dict[str, Any]] = None
    execution_time_seconds: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    experiments: List[ExperimentRunResponse] = []

    class Config:
        from_attributes = True
