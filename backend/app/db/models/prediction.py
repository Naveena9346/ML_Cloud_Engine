from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4())


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    deployment_id = Column(String(36), ForeignKey("model_deployments.id", ondelete="CASCADE"), nullable=False, index=True)
    input_payload = Column(JSON, nullable=False)
    prediction_output = Column(JSON, nullable=False)
    probabilities = Column(JSON, nullable=True)
    latency_ms = Column(Float, nullable=False, default=0.0)
    status_code = Column(String(10), nullable=False, default="200")
    
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    deployment = relationship("ModelDeployment", back_populates="prediction_logs")


class DriftReport(Base):
    __tablename__ = "drift_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    deployment_id = Column(String(36), ForeignKey("model_deployments.id", ondelete="CASCADE"), nullable=False, index=True)
    drift_score = Column(Float, nullable=False, default=0.0) # PSI or Wasserstein score
    drift_detected = Column(String(10), nullable=False, default="FALSE") # TRUE, FALSE
    feature_drift_details = Column(JSON, nullable=True) # Per-feature KS-test p-values & PSI metrics
    samples_analyzed = Column(Float, nullable=False, default=0)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    deployment = relationship("ModelDeployment", back_populates="drift_reports")
