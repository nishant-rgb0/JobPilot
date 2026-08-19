from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models import Application, User, ApplicationStatus
from auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application.status, func.count(Application.id))
        .where(Application.user_id == current_user.id)
        .group_by(Application.status)
    )
    status_counts = {status.value: count for status, count in result.all()}

    total = sum(status_counts.values())
    responded = total - status_counts.get(ApplicationStatus.applied.value, 0)
    response_rate = round((responded / total) * 100, 1) if total > 0 else 0

    return {
        "total_applications": total,
        "status_breakdown": status_counts,
        "response_rate_percent": response_rate,
    }

@router.get("/by-source")
async def get_by_source(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application.source, func.count(Application.id))
        .where(Application.user_id == current_user.id)
        .group_by(Application.source)
    )
    return {source or "unknown": count for source, count in result.all()}