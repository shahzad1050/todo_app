from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, min_length=1)
    username: str = Field(unique=True, min_length=1)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str = Field(min_length=1)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __setattr__(self, name, value):
        if name == "updated_at":
            super().__setattr__(name, datetime.utcnow())
        elif name != "updated_at":
            super().__setattr__(name, value)