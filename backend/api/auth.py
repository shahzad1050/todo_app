import sys
import os
from pathlib import Path
# Add backend directory to path to resolve relative imports
backend_dir = Path(__file__).parent.parent
backend_path = str(backend_dir.resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from core.security import create_access_token, verify_password, get_password_hash, verify_token
from pydantic import BaseModel
from datetime import timedelta
import uuid

router = APIRouter()
security = HTTPBearer()

# Simple in-memory user store for demo purposes
# In a real application, this would be stored in a database
users_db = {}

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user_data: UserRegistration) -> Dict[str, Any]:
    """
    Register a new user
    """
    # Check if user already exists
    if user_data.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_data.password)

    users_db[user_data.username] = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password
    }

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_id, "username": user_data.username},
        expires_delta=access_token_expires
    )

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login")
async def login(user_data: UserLogin) -> Dict[str, Any]:
    """
    Authenticate user and return access token
    """
    # Check if user exists
    if user_data.username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = users_db[user_data.username]

    # Verify password
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["id"], "username": user["username"]},
        expires_delta=access_token_expires
    )

    return {
        "message": "Login successful",
        "user_id": user["id"],
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
async def get_profile(credentials: HTTPAuthorizationCredentials = security) -> Dict[str, Any]:
    """
    Get user profile information
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    username = payload.get("username")

    # Find user by ID
    user = None
    for u in users_db.values():
        if u["id"] == user_id:
            user = u
            break

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = security) -> Dict[str, Any]:
    """
    Logout user (currently just a placeholder since tokens are stateless)
    """
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Logged out successfully"}