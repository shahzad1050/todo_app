from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, update
from typing import List
from uuid import UUID
from models import Task, TaskBase, User
from database import get_session
from auth_middleware import get_current_user_id, require_user_task_access
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str = None

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    is_completed: bool = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str = None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

class TaskCompletionUpdate(BaseModel):
    is_completed: bool


@router.get("/users/{user_id}/tasks", response_model=TaskListResponse)
def list_tasks(user_id: str, session: Session = Depends(get_session)):
    """Get all tasks for a specific user"""
    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get tasks for the user
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()

    # Convert to response format
    task_responses = [
        TaskResponse(
            id=task.id,
            user_id=str(task.user_id),
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

    return TaskListResponse(tasks=task_responses)

@router.post("/users/{user_id}/tasks", response_model=TaskResponse)
def create_task(user_id: str, task_data: TaskCreate, session: Session = Depends(get_session)):
    """Create a new task for a specific user"""
    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create the task
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=str(task.user_id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.get("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(user_id: str, task_id: int, session: Session = Depends(get_session)):
    """Get a specific task for a user"""
    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to user"
        )

    return TaskResponse(
        id=task.id,
        user_id=str(task.user_id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(user_id: str, task_id: int, task_data: TaskUpdate, session: Session = Depends(get_session)):
    """Update a specific task for a user"""
    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to user"
        )

    # Update the task with provided data
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=str(task.user_id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.delete("/users/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: int, session: Session = Depends(get_session)):
    """Delete a specific task for a user"""
    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to user"
        )

    # Delete the task
    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}

@router.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(user_id: str, task_id: int, completion_data: TaskCompletionUpdate, session: Session = Depends(get_session)):
    """Toggle completion status of a specific task"""
    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to user"
        )

    # Update completion status
    task.is_completed = completion_data.is_completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=str(task.user_id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )