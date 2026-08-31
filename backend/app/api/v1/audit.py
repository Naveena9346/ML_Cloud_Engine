from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.rbac import Permission, RoleChecker
from app.db.models.audit import AuditLog
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit Trails & Logging"])


@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve system audit logs for compliance tracking."""
    RoleChecker(required_permissions=[Permission.VIEW_AUDIT_LOGS])(current_user.role)

    stmt = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()
