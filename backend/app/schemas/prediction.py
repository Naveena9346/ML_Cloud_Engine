from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class RealTimePredictionRequest(BaseModel):
    features: Dict[str, Any]  # Key-value pair of feature name -> input value


class BatchPredictionRequest(BaseModel):
    dataset_version_id: str
    output_destination: Optional[str] = None


class PredictionResponse(BaseModel):
    prediction: Any
    probabilities: Optional[Dict[str, float]] = None
    latency_ms: float
    model_version: int
    endpoint_name: str


class PredictionLogResponse(BaseModel):
    id: str
    deployment_id: str
    input_payload: Dict[str, Any]
    prediction_output: Dict[str, Any]
    probabilities: Optional[Dict[str, float]] = None
    latency_ms: float
    status_code: str
    timestamp: datetime

    class Config:
        from_attributes = True


class DriftReportResponse(BaseModel):
    id: str
    deployment_id: str
    drift_score: float
    drift_detected: str
    feature_drift_details: Optional[Dict[str, Any]] = None
    samples_analyzed: float
    created_at: datetime

    class Config:
        from_attributes = True
