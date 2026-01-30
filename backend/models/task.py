from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(...)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Update updated_at timestamp before each update
    def __setattr__(self, name, value):
        if name == "updated_at":
            super().__setattr__(name, datetime.utcnow())
        elif name != "updated_at":
            super().__setattr__(name, value)