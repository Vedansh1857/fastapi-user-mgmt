from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.models import Base
import enum

class SessionStatus(str, enum.Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"
    completed = "completed"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("users.id"))
    coachee_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String(255))
    location = Column(String(255))
    capacity = Column(Integer)
    time = Column(DateTime)
    status = Column(Enum(SessionStatus), default=SessionStatus.requested)

    coach = relationship("User", foreign_keys=[coach_id])
    coachee = relationship("User", foreign_keys=[coachee_id])
