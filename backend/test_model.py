#!/usr/bin/env python3
"""Simple test to verify the Task model works"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

print("Testing Task model definition...")

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

print("Task model defined successfully!")
print("Creating a sample instance...")
sample_task = Task(title="Test Task", user_id="test-user")
print(f"Sample task: {sample_task.title}")
print("Model test completed successfully!")