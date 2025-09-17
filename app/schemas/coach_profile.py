from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import Optional

# Enum for availability status
class AvailabilityEnum(str, Enum):
    available = "available"
    unavailable = "unavailable"

class CoachProfileCreate(BaseModel):
    bio: Optional[str] = None
    expertise: Optional[str] = None
    location: Optional[str] = None
    availability: AvailabilityEnum = AvailabilityEnum.available
    image_url: Optional[HttpUrl] = None  # Image URL

class CoachProfileUpdate(BaseModel):
    bio: Optional[str] = None
    expertise: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[AvailabilityEnum] = AvailabilityEnum.available
    image_url: Optional[HttpUrl] = None  # Image URL

class CoachProfileResponse(CoachProfileCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True  # To convert SQLAlchemy models to Pydantic models
