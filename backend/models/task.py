from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# Define Task model using the most basic SQLModel pattern to avoid annotation issues
class TaskBase(SQLModel):
    title: str = Field(sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None, sa_column_kwargs={"nullable": True})
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __setattr__(self, name, value):
        if name == "updated_at":
            super().__setattr__(name, datetime.utcnow())
        elif name != "updated_at":
            super().__setattr__(name, value)