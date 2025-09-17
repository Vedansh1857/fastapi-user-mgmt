from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from sqlalchemy.orm import Session

# Create a new user
def create_user_service(user: UserCreate, db: Session) -> UserResponse:
    user_repo = UserRepository(db)
    db_user = user_repo.create_user(user, hashed_password=user.password)
    return db_user

# Get user by ID
def get_user_service(user_id: int, db: Session) -> UserResponse:
    user_repo = UserRepository(db)
    db_user = user_repo.get_user_by_id(user_id)
    if db_user is None:
        raise ValueError("User not found")
    return db_user
