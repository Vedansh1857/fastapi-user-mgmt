from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum


# Enum for session status
class SessionStatus(str, enum.Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"
    completed = "completed"


class SessionBase(BaseModel):
    topic: str
    location: str
    capacity: int
    time: datetime
    status: Optional[SessionStatus] = SessionStatus.requested  # Default status is 'requested'


class SessionCreate(SessionBase):
    coachee_id: int  # Required: coachee who is requesting the session


class SessionUpdate(BaseModel):
    topic: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    time: Optional[datetime] = None
    status: Optional[SessionStatus] = None


class SessionResponse(SessionBase):
    id: int
    coach_id: int
    coachee_id: int

    class Config:
        orm_mode = True  # To convert SQLAlchemy models to Pydantic models
