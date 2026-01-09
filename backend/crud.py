from sqlmodel import Session, select
from .models import Task, User
from typing import Optional
from uuid import UUID
from datetime import datetime

def add_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Task:
    """Add a new task for a user"""
    try:
        # Verify user ID format
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Verify the user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Create the task
    task = Task(
        title=title,
        description=description,
        user_id=user_uuid
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, user_id: str, task_id: int) -> bool:
    """Delete a task for a user"""
    try:
        # Verify user ID format
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise ValueError("Task not found")

    # Verify the task belongs to the user
    if str(task.user_id) != user_id:
        raise ValueError("Access denied: Task does not belong to user")

    # Delete the task
    session.delete(task)
    session.commit()
    return True

def update_task(session: Session, user_id: str, task_id: int, title: Optional[str] = None,
                description: Optional[str] = None, is_completed: Optional[bool] = None) -> Optional[Task]:
    """Update a task for a user"""
    try:
        # Verify user ID format
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise ValueError("Task not found")

    # Verify the task belongs to the user
    if str(task.user_id) != user_id:
        raise ValueError("Access denied: Task does not belong to user")

    # Update the task with provided data
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if is_completed is not None:
        task.is_completed = is_completed

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def list_tasks(session: Session, user_id: str, status: str = "all") -> list[Task]:
    """List tasks for a user, optionally filtered by status"""
    try:
        # Verify user ID format
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Verify the user exists
    user = session.get(User, user_uuid)
    if not user:
        raise ValueError("User not found")

    # Build query based on status filter
    query = select(Task).where(Task.user_id == user_uuid)

    if status == "completed":
        query = query.where(Task.is_completed == True)
    elif status == "pending":
        query = query.where(Task.is_completed == False)

    # Execute query
    tasks = session.exec(query).all()
    return tasks

def toggle_task_completion(session: Session, user_id: str, task_id: int) -> Optional[Task]:
    """Toggle completion status of a task for a user"""
    try:
        # Verify user ID format
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise ValueError("Task not found")

    # Verify the task belongs to the user
    if str(task.user_id) != user_id:
        raise ValueError("Access denied: Task does not belong to user")

    # Toggle completion status
    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task