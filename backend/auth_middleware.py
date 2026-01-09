from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import verify_token
from typing import Dict, Any

security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get the current user ID from the token"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

def verify_user_owns_task(user_id: str, task_user_id: str) -> bool:
    """Verify that the user owns the task"""
    return str(user_id) == str(task_user_id)

def require_user_task_access(user_id: str, task_user_id: str):
    """Raise an exception if the user doesn't have access to the task"""
    if not verify_user_owns_task(user_id, task_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to user"
        )