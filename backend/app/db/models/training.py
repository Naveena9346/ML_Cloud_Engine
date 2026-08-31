from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4())


class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_version_id = Column(String(36), ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    algorithm = Column(String(100), nullable=False) # RANDOM_FOREST, XGBOOST, LIGHTGBM, PYTORCH_NN, LOGISTIC_REGRESSION
    target_column = Column(String(255), nullable=False)
    model_type = Column(String(50), nullable=False, default="CLASSIFICATION") # CLASSIFICATION, REGRESSION
    status = Column(String(50), nullable=False, default="PENDING", index=True) # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
    
    hyperparameters = Column(JSON, nullable=True) # Selected parameters or Optuna trial space
    hyperparameter_tuning = Column(JSON, nullable=True) # Optuna search settings (n_trials, search_strategy)
    
    execution_time_seconds = Column(Float, nullable=True, default=0.0)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="training_jobs")
    dataset_version = relationship("DatasetVersion", back_populates="training_jobs")
    experiments = relationship("ExperimentRun", back_populates="training_job", cascade="all, delete-orphan")


class ExperimentRun(Base):
    __tablename__ = "experiment_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    training_job_id = Column(String(36), ForeignKey("training_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    run_name = Column(String(255), nullable=False)
    run_number = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="RUNNING")
    
    parameters = Column(JSON, nullable=True) # Actual parameters used for this run
    metrics = Column(JSON, nullable=True)    # Accuracy, F1, Precision, Recall, ROC-AUC, RMSE, MAE, R2
    artifacts = Column(JSON, nullable=True)  # Model file path, confusion matrix plot path, feature importance
    epoch_logs = Column(JSON, nullable=True) # Loss per epoch for PyTorch/iterative models
    
    duration_seconds = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    training_job = relationship("TrainingJob", back_populates="experiments")
    registered_models = relationship("ModelVersion", back_populates="experiment_run")
