from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# Schema for creating a user
class UserCreate(BaseModel):
    name: str

# Schema for returning user data
class UserResponse(BaseModel):
    id: int
    name: str
    email: str  # Include email
    phone: Optional[str]  # Include phone

    class Config:
        orm_mode = True  # This tells Pydantic to treat the SQLAlchemy models like dicts

class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None  # Optional, for phone verification
    password: constr(min_length=8)  # Password should be at least 8 characters
    name: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str