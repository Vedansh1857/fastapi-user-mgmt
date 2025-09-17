from sqlalchemy import Column, Integer, String
from app.db.sessions import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)  # Optional phone number
    password = Column(String)  # Hashed password
