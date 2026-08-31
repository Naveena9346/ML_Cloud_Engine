import os
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.dataset import DatasetVersion
from app.db.models.user import User
from app.db.session import get_db
from ml_pipelines.preprocessing.eda import EDAEngine

router = APIRouter(prefix="/eda", tags=["Exploratory Data Analysis"])


@router.get("/{dataset_version_id}", response_model=Dict[str, Any])
async def run_eda_analysis(
    dataset_version_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate statistical profiling, schema summaries, and correlation metrics for a dataset version."""
    RoleChecker(required_permissions=[Permission.RUN_EDA])(current_user.role)

    ver_res = await db.execute(select(DatasetVersion).where(DatasetVersion.id == dataset_version_id))
    version = ver_res.scalars().first()
    if not version or not os.path.exists(version.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version file snapshot not found")

    df = pd.read_csv(version.file_path)
    eda = EDAEngine(df)
    summary = eda.generate_summary()

    # Save summary into DB version
    version.eda_summary = summary
    await db.commit()

    return summary
