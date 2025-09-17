from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import Optional

# Enum to define the roles for API validation
class RoleEnum(str, Enum):
    coach = "coach"
    coachee = "coachee"

# Schema for returning user data
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr  # Include email
    phone: Optional[str]  # Include phone
    role: RoleEnum  # Include role

    class Config:
        orm_mode = True  # This tells Pydantic to treat the SQLAlchemy models like dicts

class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None  # Optional, for phone verification
    password: str  # Password should be at least 8 characters
    name: str
    role: RoleEnum  # Default role is "coachee"

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str