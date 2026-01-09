from datetime import datetime, timedelta
from typing import Optional
import uuid
from sqlmodel import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import bcrypt directly for more reliable password hashing
import bcrypt

# Create a custom password hashing function using bcrypt directly
def hash_password_direct(password: str) -> str:
    """Hash a password directly using bcrypt, ensuring it's not longer than 72 bytes"""
    # Ensure password is not longer than 72 bytes before hashing
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes max
        password_bytes = password_bytes[:72]
        # Decode back to string, handling potential multi-byte character issues
        password = password_bytes.decode('utf-8', errors='ignore')
    else:
        password = password_bytes.decode('utf-8')

    # Hash with bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password_direct(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash using bcrypt directly"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Use bcrypt directly to avoid passlib/bcrypt compatibility issues
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Hash a plain password, ensuring it's not longer than 72 bytes"""
    # Ensure password is not longer than 72 bytes before hashing
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes max
        password_bytes = password_bytes[:72]
        # Decode back to string, handling potential multi-byte character issues
        password = password_bytes.decode('utf-8', errors='ignore')
    else:
        password = password_bytes.decode('utf-8')

    # Hash with bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return the payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_user_id() -> str:
    """Generate a unique user ID"""
    return str(uuid.uuid4())

def format_response(success: bool, message: str, data: Optional[dict] = None) -> dict:
    """Format a standardized response"""
    response = {
        "success": success,
        "message": message
    }
    if data:
        response["data"] = data
    return response