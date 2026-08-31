from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.model import ModelRegistry, ModelVersion
from app.db.models.training import ExperimentRun
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.model import ModelRegisterRequest, ModelRegistryResponse, ModelStageUpdateRequest, ModelVersionResponse

router = APIRouter(prefix="/models", tags=["Model Registry & Versioning"])


@router.post("/register", response_model=ModelVersionResponse, status_code=status.HTTP_201_CREATED)
async def register_model_version(
    reg_in: ModelRegisterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Register trained model experiment run into Model Registry with version snapshot."""
    RoleChecker(required_permissions=[Permission.REGISTER_MODEL])(current_user.role)

    # Fetch experiment run
    exp_res = await db.execute(select(ExperimentRun).where(ExperimentRun.id == reg_in.experiment_run_id))
    exp_run = exp_res.scalars().first()
    if not exp_run or not exp_run.artifacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment run or artifact missing")

    # Find or create registry entry
    reg_stmt = select(ModelRegistry).where(ModelRegistry.project_id == reg_in.project_id, ModelRegistry.name == reg_in.name)
    reg_res = await db.execute(reg_stmt)
    registry = reg_res.scalars().first()

    if not registry:
        registry = ModelRegistry(
            project_id=reg_in.project_id,
            name=reg_in.name,
            description=reg_in.description,
            model_type="CLASSIFICATION",
            framework="SKLEARN"
        )
        db.add(registry)
        await db.commit()
        await db.refresh(registry)

    # Calculate next version number
    ver_cnt_res = await db.execute(select(ModelVersion).where(ModelVersion.model_registry_id == registry.id))
    versions = ver_cnt_res.scalars().all()
    next_ver = len(versions) + 1

    model_ver = ModelVersion(
        model_registry_id=registry.id,
        experiment_run_id=exp_run.id,
        version_number=next_ver,
        stage="STAGING",
        artifact_path=exp_run.artifacts.get("artifact_path", ""),
        signature_schema=exp_run.parameters or {},
        metrics=exp_run.metrics,
        tags=reg_in.tags or {"registered_by": current_user.email}
    )
    db.add(model_ver)
    await db.commit()
    await db.refresh(model_ver)
    return model_ver


@router.get("/registry", response_model=List[ModelRegistryResponse])
async def list_model_registries(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List model registries and versions for a project."""
    stmt = select(ModelRegistry).where(ModelRegistry.project_id == project_id)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.put("/versions/{version_id}/stage", response_model=ModelVersionResponse)
async def update_model_version_stage(
    version_id: str,
    stage_in: ModelStageUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Promote or transition model version stage (DRAFT -> STAGING -> PRODUCTION -> ARCHIVED)."""
    RoleChecker(required_permissions=[Permission.APPROVE_MODEL_PROMOTION])(current_user.role)

    stmt = select(ModelVersion).where(ModelVersion.id == version_id)
    res = await db.execute(stmt)
    version = res.scalars().first()
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model version not found")

    version.stage = stage_in.target_stage.upper()
    await db.commit()
    await db.refresh(version)
    return version
