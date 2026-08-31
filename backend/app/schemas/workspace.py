from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.user import UserResponse


class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkspaceMemberAdd(BaseModel):
    user_email: str
    role: str = "DEVELOPER"


class WorkspaceMemberResponse(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    role: str
    joined_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True


class WorkspaceResponse(WorkspaceBase):
    id: str
    slug: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
