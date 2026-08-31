from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import re

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.project import Project
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects Management"])


def slugify(text: str) -> str:
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new machine learning project inside a workspace."""
    RoleChecker(required_permissions=[Permission.CREATE_PROJECT])(current_user.role)

    slug = slugify(project_in.name)
    project = Project(
        workspace_id=project_in.workspace_id,
        owner_id=current_user.id,
        name=project_in.name,
        slug=slug,
        description=project_in.description,
        status="ACTIVE"
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/", response_model=List[ProjectResponse])
async def list_workspace_projects(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all ML projects within a specified workspace."""
    stmt = select(Project).where(Project.workspace_id == workspace_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_details(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve details for a specific ML project."""
    stmt = select(Project).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
