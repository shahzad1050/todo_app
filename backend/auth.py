from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from models import User, UserBase
from database import get_session
from utils import verify_password, get_password_hash, create_access_token, verify_token
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import timedelta

auth_router = APIRouter()
security = HTTPBearer()

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    message: str
    access_token: Optional[str] = None
    token_type: str = "bearer"

@auth_router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user - store ID without hyphens for consistency
    hashed_password = get_password_hash(user_data.password)
    user_id = str(uuid.uuid4()).replace('-', '')
    user = User(
        id=user_id,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        message="Account created successfully"
    )

@auth_router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return token"""
    # Find user by email
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create access token - ensure user ID is consistent
    user_id_for_token = str(user.id)
    access_token = create_access_token(data={"sub": user_id_for_token})

    return UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        message="Login successful",
        access_token=access_token
    )

@auth_router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user (placeholder implementation)"""
    # In a real implementation, you would invalidate the token
    return {"message": "Logout successful"}