from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas.user_schema import UserResponse
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional

# Initialize password context (using bcrypt hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define OAuth2PasswordBearer to extract token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT secret and algorithm settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # JWT token expiry

# Hashing password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    print(f"Data to encode in the token: {to_encode}")

    print(f"Data is: {data}")

    payload = {
        "sub": data["sub"],  # The 'sub' is typically the user's email
        "id": data.get("id"),
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "role": data.get("role"),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT token verification
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Create refresh token with a longer expiration time
def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency for extracting and verifying the current user from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    This function will extract the user info from the token
    and ensure it is a valid and authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        print(f"Decoded JWT payload: {payload}")

        # Verify the expiration of the token
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise credentials_exception
        
        user = UserResponse(
            id=payload["id"],
            name=payload["name"],
            email=payload["email"],
            phone=payload.get("phone", None),  # Optional field
            role=payload["role"]
        )
        return user

    except JWTError:
        raise credentials_exception