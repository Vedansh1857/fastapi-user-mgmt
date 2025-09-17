
import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
# from enum import Enum
from app.models import Base

# Enum to define the roles
class RoleEnum(str, enum.Enum):
    coach = "coach"
    coachee = "coachee"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)  # Optional phone number
    password = Column(String)  # Hashed password
    role = Column(Enum(RoleEnum), default=RoleEnum.coachee)  # Default to "coachee"
    coach_profile = relationship("CoachProfile", back_populates="user", uselist=False)
    coachee_profile = relationship("CoacheeProfile", back_populates="user", uselist=False)