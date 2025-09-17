from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate, hashed_password: str):
        db_user = User(
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()