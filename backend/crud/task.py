from sqlmodel import Session, select
from typing import List, Optional
from ..models import Task, TaskBase
from uuid import UUID

def create_task(session: Session, task: TaskBase) -> Task:
    """
    Create a new task in the database
    """
    db_task = Task.from_orm(task) if hasattr(Task, 'from_orm') else Task(**task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task_by_id(session: Session, task_id: UUID) -> Optional[Task]:
    """
    Get a task by its ID
    """
    statement = select(Task).where(Task.id == task_id)
    return session.exec(statement).first()

def get_tasks_by_user(session: Session, user_id: UUID, status: str = "all") -> List[Task]:
    """
    Get all tasks for a specific user, optionally filtered by status
    """
    statement = select(Task).where(Task.user_id == user_id)

    if status == "completed":
        statement = statement.where(Task.is_completed == True)
    elif status == "pending":
        statement = statement.where(Task.is_completed == False)

    statement = statement.order_by(Task.created_at.desc())
    return session.exec(statement).all()

def update_task(session: Session, task_id: UUID, task_data: TaskBase) -> Optional[Task]:
    """
    Update an existing task
    """
    db_task = get_task_by_id(session, task_id)
    if not db_task:
        return None

    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: UUID) -> bool:
    """
    Delete a task by its ID
    """
    db_task = get_task_by_id(session, task_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True

def toggle_task_completion(session: Session, task_id: UUID) -> Optional[Task]:
    """
    Toggle the completion status of a task
    """
    db_task = get_task_by_id(session, task_id)
    if not db_task:
        return None

    db_task.is_completed = not db_task.is_completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task