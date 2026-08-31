import os
from fastapi import APIRouter, Depends, HTTPException, status
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.dataset import Dataset, DatasetVersion
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.dataset import DataCleaningOptions, DatasetVersionResponse
from ml_pipelines.preprocessing.cleaner import DataCleanerEngine

router = APIRouter(prefix="/preprocessing", tags=["Data Cleaning & Preprocessing"])


@router.post("/clean/{dataset_id}", response_model=DatasetVersionResponse)
async def clean_and_preprocess_dataset(
    dataset_id: str,
    options: DataCleaningOptions,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Execute automated data cleaning, missing value imputation, outlier handling, and encoding."""
    RoleChecker(required_permissions=[Permission.CLEAN_DATASET])(current_user.role)

    # Fetch dataset and latest version
    ds_res = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = ds_res.scalars().first()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    ver_res = await db.execute(select(DatasetVersion).where(DatasetVersion.dataset_id == dataset_id).order_by(DatasetVersion.version_number.desc()))
    current_ver = ver_res.scalars().first()
    if not current_ver or not os.path.exists(current_ver.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raw dataset snapshot file missing")

    # Load dataframe & execute cleaner engine
    df = pd.read_csv(current_ver.file_path)
    cleaner = DataCleanerEngine(df)
    cleaned_df, logs = cleaner.execute_pipeline(options.model_dump())

    # Save cleaned file snapshot
    cleaned_filename = f"cleaned_v{dataset.current_version + 1}_{os.path.basename(current_ver.file_path)}"
    cleaned_path = os.path.join(os.path.dirname(current_ver.file_path), cleaned_filename)
    cleaned_df.to_csv(cleaned_path, index=False)

    # Create new Dataset Version
    new_version_num = dataset.current_version + 1
    dataset.current_version = new_version_num

    new_version = DatasetVersion(
        dataset_id=dataset.id,
        version_number=new_version_num,
        file_path=cleaned_path,
        file_size_bytes=os.path.getsize(cleaned_path),
        row_count=len(cleaned_df),
        column_count=len(cleaned_df.columns),
        schema_json={col: str(dtype) for col, dtype in cleaned_df.dtypes.items()},
        cleaned_status="CLEANED"
    )
    db.add(new_version)
    await db.commit()
    await db.refresh(new_version)
    return new_version
