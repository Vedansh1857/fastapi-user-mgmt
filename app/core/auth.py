from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional

# Initialize password context (using bcrypt hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
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
