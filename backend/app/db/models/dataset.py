from datetime import datetime, timezone
import uuid
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4())


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    data_type = Column(String(50), nullable=False, default="TABULAR")  # TABULAR, TEXT, IMAGE, TIME_SERIES
    file_format = Column(String(50), nullable=False, default="CSV")     # CSV, PARQUET, JSON, ARROW
    current_version = Column(Integer, default=1, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="datasets")
    versions = relationship("DatasetVersion", back_populates="dataset", cascade="all, delete-orphan")


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False, index=True)
    file_path = Column(String(512), nullable=False)   # Local or S3 path
    file_size_bytes = Column(BigInteger, nullable=False, default=0)
    row_count = Column(BigInteger, nullable=False, default=0)
    column_count = Column(Integer, nullable=False, default=0)
    sha256_checksum = Column(String(64), nullable=True)
    schema_json = Column(JSON, nullable=True)        # Column names, data types, null counts
    eda_summary = Column(JSON, nullable=True)         # Mean, std, quartiles, correlations
    cleaned_status = Column(String(50), default="RAW", nullable=False)  # RAW, PROCESSING, CLEANED
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    dataset = relationship("Dataset", back_populates="versions")
    feature_sets = relationship("FeatureStore", back_populates="dataset_version", cascade="all, delete-orphan")
    training_jobs = relationship("TrainingJob", back_populates="dataset_version")


class FeatureStore(Base):
    __tablename__ = "feature_store"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    dataset_version_id = Column(String(36), ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_name = Column(String(255), nullable=False, index=True)
    feature_type = Column(String(50), nullable=False)  # NUMERICAL, CATEGORICAL, DATETIME, TEXT
    transformation_rules = Column(JSON, nullable=True) # Imputation, scaling, one-hot encoding details
    sample_values = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    dataset_version = relationship("DatasetVersion", back_populates="feature_sets")
