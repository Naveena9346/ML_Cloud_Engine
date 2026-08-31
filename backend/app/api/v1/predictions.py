import os
import time
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
import joblib
import numpy as np
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.model import ModelDeployment, ModelVersion
from app.db.models.prediction import PredictionLog
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.prediction import PredictionResponse, RealTimePredictionRequest

router = APIRouter(prefix="/predictions", tags=["Real-Time & Batch Predictions"])


@router.post("/realtime/{endpoint_name}", response_model=PredictionResponse)
async def predict_realtime(
    endpoint_name: str,
    payload: RealTimePredictionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Invoke real-time inference prediction API endpoint."""
    RoleChecker(required_permissions=[Permission.INVOKE_PREDICTION_API])(current_user.role)

    start_time = time.time()

    # Locate deployment endpoint
    dep_stmt = select(ModelDeployment).where(ModelDeployment.endpoint_name == endpoint_name, ModelDeployment.status == "ACTIVE")
    dep_res = await db.execute(dep_stmt)
    deployment = dep_res.scalars().first()

    if not deployment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Active endpoint '{endpoint_name}' not found")

    # Fetch associated model version
    ver_res = await db.execute(select(ModelVersion).where(ModelVersion.id == deployment.model_version_id))
    model_ver = ver_res.scalars().first()
    if not model_ver or not os.path.exists(model_ver.artifact_path):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Model artifact file missing on server")

    # Load model artifact
    try:
        model_pack = joblib.load(model_ver.artifact_path)
        model = model_pack["model"]
        
        input_df = pd.DataFrame([payload.features])
        prediction = model.predict(input_df)[0]
        
        probabilities = None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(input_df)[0]
            probabilities = {f"class_{i}": float(p) for i, p in enumerate(probs)}

        latency = (time.time() - start_time) * 1000.0

        # Convert numpy types to python native for JSON serialization
        pred_val = int(prediction) if isinstance(prediction, (np.integer, bool)) else float(prediction)

        # Log prediction telemetry
        pred_log = PredictionLog(
            deployment_id=deployment.id,
            input_payload=payload.features,
            prediction_output={"prediction": pred_val},
            probabilities=probabilities,
            latency_ms=round(latency, 2),
            status_code="200"
        )
        db.add(pred_log)

        # Update deployment request counters
        deployment.total_requests += 1
        deployment.avg_latency_ms = int((deployment.avg_latency_ms + latency) / 2)
        await db.commit()

        return PredictionResponse(
            prediction=pred_val,
            probabilities=probabilities,
            latency_ms=round(latency, 2),
            model_version=model_ver.version_number,
            endpoint_name=endpoint_name
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Inference error: {str(e)}")
