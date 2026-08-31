import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.dataset import DatasetVersion
from app.db.models.model import ModelDeployment, ModelVersion
from app.db.models.prediction import DriftReport, PredictionLog
from app.db.models.training import ExperimentRun, TrainingJob
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.prediction import DriftReportResponse
from ml_pipelines.monitoring.drift_detector import DriftDetectorEngine

router = APIRouter(prefix="/monitoring", tags=["Model Drift & Monitoring"])


@router.post("/drift/{deployment_id}", response_model=DriftReportResponse)
async def calculate_endpoint_drift(
    deployment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Compute Population Stability Index (PSI) and KS-test drift metrics for deployed model."""
    RoleChecker(required_permissions=[Permission.VIEW_MONITORING_DASHBOARD])(current_user.role)

    # Fetch deployment & model version
    dep_res = await db.execute(select(ModelDeployment).where(ModelDeployment.id == deployment_id))
    deployment = dep_res.scalars().first()
    if not deployment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deployment not found")

    ver_res = await db.execute(select(ModelVersion).where(ModelVersion.id == deployment.model_version_id))
    model_ver = ver_res.scalars().first()

    # Fetch training dataset baseline reference
    ref_df = pd.DataFrame()
    if model_ver and model_ver.experiment_run_id:
        exp_res = await db.execute(select(ExperimentRun).where(ExperimentRun.id == model_ver.experiment_run_id))
        exp_run = exp_res.scalars().first()
        if exp_run:
            job_res = await db.execute(select(TrainingJob).where(TrainingJob.id == exp_run.training_job_id))
            job = job_res.scalars().first()
            if job:
                ds_ver_res = await db.execute(select(DatasetVersion).where(DatasetVersion.id == job.dataset_version_id))
                ds_ver = ds_ver_res.scalars().first()
                if ds_ver and os.path.exists(ds_ver.file_path):
                    ref_df = pd.read_csv(ds_ver.file_path)

    # Fetch inference logs current data
    logs_res = await db.execute(select(PredictionLog).where(PredictionLog.deployment_id == deployment_id).limit(500))
    logs = logs_res.scalars().all()
    if not logs or ref_df.empty:
        # Fallback empty report
        report = DriftReport(
            deployment_id=deployment_id,
            drift_score=0.0,
            drift_detected="FALSE",
            feature_drift_details={"info": "Insufficient prediction telemetry samples"},
            samples_analyzed=0
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    curr_df = pd.DataFrame([log.input_payload for log in logs])

    # Run drift detector engine
    detector = DriftDetectorEngine()
    drift_analysis = detector.analyze_dataset_drift(ref_df, curr_df)

    report = DriftReport(
        deployment_id=deployment_id,
        drift_score=drift_analysis["overall_drift_score"],
        drift_detected="TRUE" if drift_analysis["drift_detected"] else "FALSE",
        feature_drift_details=drift_analysis["feature_details"],
        samples_analyzed=drift_analysis["samples_analyzed"]
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/reports/{deployment_id}", response_model=List[DriftReportResponse])
async def list_drift_reports(
    deployment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List historical drift reports for an active deployment."""
    stmt = select(DriftReport).where(DriftReport.deployment_id == deployment_id).order_by(DriftReport.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()
