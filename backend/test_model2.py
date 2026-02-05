#!/usr/bin/env python3
"""Simple test to verify the Task model works with different syntax"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

print("Testing Task model definition with different syntax...")

# Try with different approach
class TaskBase(SQLModel):
    title: str = Field()
    description: Optional[str] = None
    is_completed: bool = False

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

print("Task model defined successfully!")
print("Creating a sample instance...")
sample_task = Task(title="Test Task", user_id="test-user")
print(f"Sample task: {sample_task.title}")
print("Model test completed successfully!")