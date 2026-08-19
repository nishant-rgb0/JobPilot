from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from database import get_db
from models import Application, User, ApplicationStatus
from schemas import ApplicationCreate, ApplicationUpdate, ApplicationOut
from auth import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("", response_model=ApplicationOut)
async def create_application(
    application: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    new_app = Application(
        user_id=current_user.id,
        company=application.company,
        role_title=application.role_title,
        source=application.source,
        notes=application.notes,
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app

@router.get("", response_model=List[ApplicationOut])
async def list_applications(
    status: Optional[ApplicationStatus] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Application).where(Application.user_id == current_user.id)
    if status:
        query = query.where(Application.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{application_id}", response_model=ApplicationOut)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.patch("/{application_id}", response_model=ApplicationOut)
async def update_application(
    application_id: int,
    update: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if update.status is not None:
        application.status = update.status
    if update.notes is not None:
        application.notes = update.notes

    await db.commit()
    await db.refresh(application)
    return application

@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    await db.delete(application)
    await db.commit()
    return {"detail": "Application deleted"}