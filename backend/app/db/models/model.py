from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4())


class ModelRegistry(Base):
    __tablename__ = "model_registries"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    model_type = Column(String(50), nullable=False, default="CLASSIFICATION") # CLASSIFICATION, REGRESSION
    framework = Column(String(50), nullable=False) # SKLEARN, XGBOOST, LIGHTGBM, PYTORCH
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="model_registries")
    versions = relationship("ModelVersion", back_populates="model_registry", cascade="all, delete-orphan")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    model_registry_id = Column(String(36), ForeignKey("model_registries.id", ondelete="CASCADE"), nullable=False, index=True)
    experiment_run_id = Column(String(36), ForeignKey("experiment_runs.id", ondelete="SET NULL"), nullable=True, index=True)
    version_number = Column(Integer, nullable=False, index=True)
    
    stage = Column(String(50), nullable=False, default="DRAFT", index=True) # DRAFT, STAGING, PRODUCTION, ARCHIVED
    artifact_path = Column(String(512), nullable=False) # S3 or local path to .joblib / .pt file
    signature_schema = Column(JSON, nullable=False)     # Input feature definitions & types
    metrics = Column(JSON, nullable=True)               # Performance snapshot
    tags = Column(JSON, nullable=True)                  # User custom labels
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    model_registry = relationship("ModelRegistry", back_populates="versions")
    experiment_run = relationship("ExperimentRun", back_populates="registered_models")
    deployments = relationship("ModelDeployment", back_populates="model_version", cascade="all, delete-orphan")


class ModelDeployment(Base):
    __tablename__ = "model_deployments"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    model_version_id = Column(String(36), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    endpoint_name = Column(String(255), unique=True, nullable=False, index=True)
    deployment_type = Column(String(50), nullable=False, default="REAL_TIME") # REAL_TIME, BATCH
    status = Column(String(50), nullable=False, default="ACTIVE", index=True) # ACTIVE, INACTIVE, FAILED, RETIRED
    
    api_key_hash = Column(String(255), nullable=True) # Optional endpoint authentication key hash
    replicas = Column(Integer, default=1, nullable=False)
    total_requests = Column(Integer, default=0, nullable=False)
    avg_latency_ms = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="deployments")
    model_version = relationship("ModelVersion", back_populates="deployments")
    prediction_logs = relationship("PredictionLog", back_populates="deployment", cascade="all, delete-orphan")
    drift_reports = relationship("DriftReport", back_populates="deployment", cascade="all, delete-orphan")
