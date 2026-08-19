from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

from datetime import datetime
from typing import Optional
from models import ApplicationStatus

class ApplicationCreate(BaseModel):
    company: str
    role_title: str
    source: Optional[str] = None
    notes: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    company: str
    role_title: str
    status: ApplicationStatus
    source: Optional[str]
    notes: Optional[str]
    applied_date: datetime
    last_updated: datetime

    class Config:
        from_attributes = True