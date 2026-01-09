from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# User model
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True, nullable=False)  # Will be set in auth.py
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Task model
class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Session model
class SessionBase(SQLModel):
    user_id: str = Field(foreign_key="users.id")
    expires_at: datetime

class Session(SessionBase, table=True):
    __tablename__ = "sessions"

    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)