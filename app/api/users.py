from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.user_service import create_user_service, get_user_service
from app.core.auth import verify_password, create_access_token, create_refresh_token
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.db.sessions import SessionLocal
from app.schemas.user_schema import UserCreate
from app.core.auth import hash_password
from app.core.config import settings
from jose import JWTError, jwt

router = APIRouter()

# Dependency for getting the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_service(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register/", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash password before storing
    hashed_password = hash_password(user.password)
    
    user_repo = UserRepository(db)
    db_user = user_repo.create_user(user, hashed_password)
    
    if db_user:
        return {"message": "User created successfully"}
    raise HTTPException(status_code=400, detail="User could not be created")

# Login API
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    db_user = user_repo.get_user_by_email(user.email)
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token if the password is correct
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

class RefreshTokenRequest(BaseModel):
    refresh_token: str  # Expect the refresh_token in the request body

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        # Ensure the refresh token is valid and not expired
        new_access_token = create_access_token(data={"sub": payload["sub"]})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")