from datetime import datetime
from enum import Enum
from pydantic import BaseModel, HttpUrl, Field


class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=255)
    role: str = Field(min_length=1, max_length=255)
    status: ApplicationStatus = ApplicationStatus.APPLIED
    link: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=2000)


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=255)
    role: str | None = Field(default=None, min_length=1, max_length=255)
    status: ApplicationStatus | None = None
    link: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=2000)


class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: ApplicationStatus
    link: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True