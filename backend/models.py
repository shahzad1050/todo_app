from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# User model
class UserBase(SQLModel):
    email: str = Field(min_length=1)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True)  # Will be set in auth.py
    hashed_password: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Task model
class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Session model
class SessionBase(SQLModel):
    user_id: str = Field(min_length=1)
    expires_at: datetime = Field(...)

class Session(SessionBase, table=True):
    __tablename__ = "sessions"

    id: str = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)