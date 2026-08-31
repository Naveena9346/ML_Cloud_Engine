from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.model import ModelDeployment, ModelVersion
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.model import ModelDeploymentCreate, ModelDeploymentResponse

router = APIRouter(prefix="/deployments", tags=["Model Deployment & Endpoint Serving"])


@router.post("/", response_model=ModelDeploymentResponse, status_code=status.HTTP_201_CREATED)
async def create_model_deployment(
    deploy_in: ModelDeploymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deploy model version to real-time or batch prediction endpoint."""
    RoleChecker(required_permissions=[Permission.DEPLOY_MODEL_ENDPOINT])(current_user.role)

    # Check endpoint name uniqueness
    existing = await db.execute(select(ModelDeployment).where(ModelDeployment.endpoint_name == deploy_in.endpoint_name))
    if existing.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Endpoint name already in use")

    # Validate model version exists
    ver_res = await db.execute(select(ModelVersion).where(ModelVersion.id == deploy_in.model_version_id))
    version = ver_res.scalars().first()
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model version not found")

    deployment = ModelDeployment(
        project_id=deploy_in.project_id,
        model_version_id=deploy_in.model_version_id,
        endpoint_name=deploy_in.endpoint_name,
        deployment_type=deploy_in.deployment_type,
        status="ACTIVE",
        replicas=deploy_in.replicas
    )
    db.add(deployment)
    await db.commit()
    await db.refresh(deployment)
    return deployment


@router.get("/", response_model=List[ModelDeploymentResponse])
async def list_project_deployments(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List active endpoints deployed under a project."""
    stmt = select(ModelDeployment).where(ModelDeployment.project_id == project_id)
    res = await db.execute(stmt)
    return res.scalars().all()
