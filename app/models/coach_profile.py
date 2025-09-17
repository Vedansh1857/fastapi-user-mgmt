from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base
import enum

class AvailabilityEnum(str, enum.Enum):
    available = "available"
    unavailable = "unavailable"

class CoachProfile(Base):
    __tablename__ = "coach_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Foreign key to User
    bio = Column(Text, nullable=True)
    expertise = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    availability = Column(Enum(AvailabilityEnum), default=AvailabilityEnum.available)  # Enum: available/unavailable
    image_url = Column(String(255), nullable=True)  # URL of the uploaded image
    
    # Define relationship to User model (One-to-One or One-to-Many depending on your needs)
    user = relationship("User", back_populates="coach_profile")
