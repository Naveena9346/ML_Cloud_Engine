import hashlib
import os
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.config import settings
from app.core.rbac import Permission, RoleChecker
from app.db.models.dataset import Dataset, DatasetVersion, FeatureStore
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.dataset import DatasetCreate, DatasetResponse, DatasetVersionResponse

router = APIRouter(prefix="/datasets", tags=["Dataset Management & Storage"])

UPLOAD_DIR = os.path.join(os.getcwd(), "data_storage")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset_file(
    project_id: str = Form(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    data_type: str = Form("TABULAR"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload dataset file (CSV/Parquet/JSON) and register initial version snapshot."""
    RoleChecker(required_permissions=[Permission.UPLOAD_DATASET])(current_user.role)

    # Read uploaded bytes and calculate SHA-256 hash
    content = await file.read()
    sha256_hash = hashlib.sha256(content).hexdigest()
    
    file_ext = os.path.splitext(file.filename)[1].lower() or ".csv"
    save_filename = f"{sha256_hash[:16]}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, save_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    # Parse dataset basic statistics with pandas
    row_count = 0
    col_count = 0
    schema_json = {}
    
    try:
        if file_ext == ".csv":
            df = pd.read_csv(file_path, nrows=500)
            row_count = len(pd.read_csv(file_path, usecols=[0]))
        elif file_ext == ".parquet":
            df = pd.read_parquet(file_path)
            row_count = len(df)
        else:
            df = pd.read_json(file_path)
            row_count = len(df)

        col_count = len(df.columns)
        schema_json = {col: str(dtype) for col, dtype in df.dtypes.items()}
    except Exception as e:
        schema_json = {"error": f"Failed to parse file schema: {str(e)}"}

    # Create Dataset Record
    dataset = Dataset(
        project_id=project_id,
        name=name,
        description=description,
        data_type=data_type,
        file_format=file_ext.replace(".", "").upper(),
        current_version=1
    )
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)

    # Create Initial Version Snapshot
    version = DatasetVersion(
        dataset_id=dataset.id,
        version_number=1,
        file_path=file_path,
        file_size_bytes=len(content),
        row_count=row_count,
        column_count=col_count,
        sha256_checksum=sha256_hash,
        schema_json=schema_json,
        cleaned_status="RAW"
    )
    db.add(version)
    await db.commit()
    await db.refresh(version)

    dataset.latest_version = version
    return dataset


@router.get("/", response_model=List[DatasetResponse])
async def list_project_datasets(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List datasets registered under a specified project."""
    stmt = select(Dataset).where(Dataset.project_id == project_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{dataset_id}/preview")
async def preview_dataset_rows(
    dataset_id: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Preview first N rows of a dataset snapshot."""
    stmt = select(DatasetVersion).where(DatasetVersion.dataset_id == dataset_id).order_by(DatasetVersion.version_number.desc())
    res = await db.execute(stmt)
    version = res.scalars().first()

    if not version or not os.path.exists(version.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset file snapshot not found")

    df = pd.read_csv(version.file_path, nrows=limit)
    return {
        "columns": list(df.columns),
        "data": df.fillna("").to_dict(orient="records"),
        "total_preview_rows": len(df)
    }
