import os
import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import joblib
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.dataset import DatasetVersion
from app.db.models.training import ExperimentRun, TrainingJob
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.training import TrainingJobCreate, TrainingJobResponse
from ml_pipelines.evaluation.evaluator import ModelEvaluatorEngine
from ml_pipelines.training.optuna_tuner import OptunaTunerEngine
from ml_pipelines.training.trainer import ModelTrainerEngine

router = APIRouter(prefix="/training", tags=["Model Training & Experiments"])

MODELS_DIR = os.path.join(os.getcwd(), "models_storage")
os.makedirs(MODELS_DIR, exist_ok=True)


@router.post("/jobs", response_model=TrainingJobResponse, status_code=status.HTTP_201_CREATED)
async def create_training_job(
    job_in: TrainingJobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Launch model training job with optional Optuna hyperparameter optimization."""
    RoleChecker(required_permissions=[Permission.START_TRAINING_JOB])(current_user.role)

    # Validate dataset version exists
    ver_res = await db.execute(select(DatasetVersion).where(DatasetVersion.id == job_in.dataset_version_id))
    dataset_version = ver_res.scalars().first()
    if not dataset_version or not os.path.exists(dataset_version.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset snapshot file not found")

    df = pd.read_csv(dataset_version.file_path)
    if job_in.target_column not in df.columns:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Target column '{job_in.target_column}' missing from dataset")

    # Create TrainingJob record
    job = TrainingJob(
        project_id=job_in.project_id,
        dataset_version_id=job_in.dataset_version_id,
        name=job_in.name,
        algorithm=job_in.algorithm,
        target_column=job_in.target_column,
        model_type=job_in.model_type,
        status="RUNNING",
        hyperparameters=job_in.hyperparameters
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    start_time = time.time()
    best_params = job_in.hyperparameters or {}

    try:
        # Run Optuna tuning if requested
        if job_in.enable_tuning:
            tuner = OptunaTunerEngine(df, job_in.target_column, job_in.algorithm, job_in.model_type)
            tuning_res = tuner.optimize(n_trials=job_in.tuning_trials)
            best_params.update(tuning_res.get("best_params", {}))
            job.hyperparameter_tuning = tuning_res

        # Train model
        trainer = ModelTrainerEngine(df, job_in.target_column, job_in.model_type)
        model, eval_results, X_train, y_train = trainer.train(job_in.algorithm, best_params)
        
        # Evaluate model metrics
        if job_in.model_type.upper() == "CLASSIFICATION":
            metrics = ModelEvaluatorEngine.evaluate_classification(
                eval_results["y_test"], eval_results["y_pred"], eval_results["y_proba"]
            )
        else:
            metrics = ModelEvaluatorEngine.evaluate_regression(
                eval_results["y_test"], eval_results["y_pred"]
            )

        # Save trained model artifact to file
        model_filename = f"job_{job.id}_{job_in.algorithm.lower()}.joblib"
        artifact_path = os.path.join(MODELS_DIR, model_filename)
        
        signature_schema = {col: str(dtype) for col, dtype in X_train.dtypes.items()}
        joblib.dump({"model": model, "signature": signature_schema, "target": job_in.target_column}, artifact_path)

        exec_time = time.time() - start_time
        job.status = "COMPLETED"
        job.execution_time_seconds = round(exec_time, 2)
        job.hyperparameters = best_params

        # Create Experiment Run record
        exp_run = ExperimentRun(
            training_job_id=job.id,
            run_name=f"{job_in.name}_Run_1",
            status="COMPLETED",
            parameters=best_params,
            metrics=metrics,
            artifacts={"artifact_path": artifact_path, "model_filename": model_filename},
            duration_seconds=round(exec_time, 2)
        )
        db.add(exp_run)
        await db.commit()
        await db.refresh(job)

    except Exception as e:
        job.status = "FAILED"
        job.error_message = str(e)
        await db.commit()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Training failed: {str(e)}")

    # Fetch with experiments
    res = await db.execute(select(TrainingJob).where(TrainingJob.id == job.id))
    return res.scalars().first()


@router.get("/jobs", response_model=List[TrainingJobResponse])
async def list_project_training_jobs(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List training jobs for a project."""
    stmt = select(TrainingJob).where(TrainingJob.project_id == project_id).order_by(TrainingJob.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()
