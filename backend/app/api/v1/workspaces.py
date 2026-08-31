from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import re

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.user import User
from app.db.models.workspace import Workspace, WorkspaceMember
from app.db.session import get_db
from app.schemas.workspace import WorkspaceCreate, WorkspaceMemberAdd, WorkspaceMemberResponse, WorkspaceResponse

router = APIRouter(prefix="/workspaces", tags=["Workspaces & Governance"])


def slugify(text: str) -> str:
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')


@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_in: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new workspace environment."""
    RoleChecker(required_permissions=[Permission.CREATE_WORKSPACE])(current_user.role)
    
    slug = slugify(workspace_in.name)
    existing = await db.execute(select(Workspace).where(Workspace.slug == slug))
    if existing.scalars().first():
        slug = f"{slug}-{current_user.id[:8]}"

    workspace = Workspace(
        name=workspace_in.name,
        slug=slug,
        description=workspace_in.description,
        owner_id=current_user.id,
    )
    db.add(workspace)
    await db.commit()
    await db.refresh(workspace)

    # Add owner as admin member
    member = WorkspaceMember(workspace_id=workspace.id, user_id=current_user.id, role="ADMIN")
    db.add(member)
    await db.commit()

    return workspace


@router.get("/", response_model=List[WorkspaceResponse])
async def list_user_workspaces(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List workspaces owned or joined by the current user."""
    stmt = (
        select(Workspace)
        .join(WorkspaceMember, Workspace.id == WorkspaceMember.workspace_id)
        .where(WorkspaceMember.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/{workspace_id}/members", response_model=WorkspaceMemberResponse)
async def add_workspace_member(
    workspace_id: str,
    member_in: WorkspaceMemberAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Invite a user to a workspace."""
    RoleChecker(required_permissions=[Permission.MANAGE_WORKSPACE_MEMBERS])(current_user.role)

    # Find target user by email
    user_res = await db.execute(select(User).where(User.email == member_in.user_email))
    target_user = user_res.scalars().first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with provided email not found")

    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=target_user.id,
        role=member_in.role
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member
