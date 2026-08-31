from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelRegisterRequest(BaseModel):
    project_id: str
    experiment_run_id: str
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None


class ModelStageUpdateRequest(BaseModel):
    target_stage: str  # DRAFT, STAGING, PRODUCTION, ARCHIVED


class ModelVersionResponse(BaseModel):
    id: str
    model_registry_id: str
    experiment_run_id: Optional[str] = None
    version_number: int
    stage: str
    artifact_path: str
    signature_schema: Dict[str, Any]
    metrics: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ModelRegistryResponse(BaseModel):
    id: str
    project_id: str
    name: str
    description: Optional[str] = None
    model_type: str
    framework: str
    created_at: datetime
    updated_at: datetime
    versions: List[ModelVersionResponse] = []

    class Config:
        from_attributes = True


class ModelDeploymentCreate(BaseModel):
    project_id: str
    model_version_id: str
    endpoint_name: str = Field(..., min_length=2, max_length=255)
    deployment_type: str = "REAL_TIME"  # REAL_TIME, BATCH
    replicas: int = 1


class ModelDeploymentResponse(BaseModel):
    id: str
    project_id: str
    model_version_id: str
    endpoint_name: str
    deployment_type: str
    status: str
    replicas: int
    total_requests: int
    avg_latency_ms: int
    created_at: datetime
    updated_at: datetime
    model_version: Optional[ModelVersionResponse] = None

    class Config:
        from_attributes = True
