import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

# Security Configurations
# In production, SECRET_KEY MUST be a long random string in your .env file!
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-hackathon-key-change-me-later")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Tokens last for 7 days

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the hashed version in the DB."""
    password_bytes = plain_password.encode('utf-8')
    # Bcrypt requires both strings to be encoded as bytes
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def get_password_hash(password: str) -> str:
    """Hashes a password for saving into the DB."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Decode back to a normal string to store in PostgreSQL
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates the JWT Token for user sessions."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt