from typing import Dict, Any, List
from uuid import UUID
from sqlmodel import Session
import sys
import os
from pathlib import Path

# Add backend directory to path to resolve relative imports
backend_dir = Path(__file__).parent.parent
backend_path = str(backend_dir.resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from core.database import engine

# Import models - using direct import since models directory was removed
from models import Task, TaskBase
from crud.task import get_tasks_by_user, create_task, update_task as update_task_crud, delete_task as delete_task_crud, toggle_task_completion
from crud.conversation import create_conversation
from crud.message import create_message, get_messages_by_conversation
from models.conversation import ConversationBase
from models.message import MessageBase, RoleEnum
from crud.task import get_tasks_by_user, create_task, update_task as update_task_crud, delete_task as delete_task_crud, toggle_task_completion
from crud.conversation import create_conversation
from crud.message import create_message, get_messages_by_conversation
from models.conversation import ConversationBase
from models.message import MessageBase, RoleEnum

def add_task_tool(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
    """
    Add a new task for a user
    """
    with Session(engine) as session:
        task_base = TaskBase(
            title=title,
            description=description,
            user_id=UUID(user_id)
        )
        task = create_task(session, task_base)

        return {
            "task_id": str(task.id),
            "status": "added",
            "title": task.title
        }

def list_tasks_tool(user_id: str, status: str = "all") -> Dict[str, List[Dict[str, Any]]]:
    """
    List tasks for a user with optional status filter
    """
    with Session(engine) as session:
        tasks = get_tasks_by_user(session, UUID(user_id), status)

        task_list = []
        for task in tasks:
            task_list.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.is_completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })

        return {
            "tasks": task_list
        }

def update_task_tool(user_id: str, task_id: str, title: str = None, description: str = None) -> Dict[str, Any]:
    """
    Update an existing task
    """
    with Session(engine) as session:
        # We need to fetch the existing task first to validate user ownership
        existing_task = session.get(Task, UUID(task_id))
        if not existing_task or str(existing_task.user_id) != user_id:
            return {
                "task_id": task_id,
                "status": "error",
                "message": "Task not found or access denied"
            }

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description

        # Create a TaskBase object with the updates
        task_update = TaskBase(
            title=update_data.get('title', existing_task.title),
            description=update_data.get('description', existing_task.description),
            is_completed=existing_task.is_completed,
            user_id=UUID(user_id)
        )

        updated_task = update_task_crud(session, UUID(task_id), task_update)

        if updated_task:
            return {
                "task_id": str(updated_task.id),
                "title": updated_task.title,
                "description": updated_task.description,
                "updated_at": updated_task.updated_at.isoformat()
            }
        else:
            return {
                "task_id": task_id,
                "status": "error",
                "message": "Failed to update task"
            }

def delete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a task
    """
    with Session(engine) as session:
        # We need to fetch the existing task first to validate user ownership
        existing_task = session.get(Task, UUID(task_id))
        if not existing_task or str(existing_task.user_id) != user_id:
            return {
                "task_id": task_id,
                "status": "error",
                "message": "Task not found or access denied"
            }

        success = delete_task_crud(session, UUID(task_id))

        if success:
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": existing_task.title
            }
        else:
            return {
                "task_id": task_id,
                "status": "error",
                "message": "Failed to delete task"
            }

def complete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Mark a task as complete or incomplete
    """
    with Session(engine) as session:
        # We need to fetch the existing task first to validate user ownership
        existing_task = session.get(Task, UUID(task_id))
        if not existing_task or str(existing_task.user_id) != user_id:
            return {
                "task_id": task_id,
                "completed": False,
                "status": "error",
                "message": "Task not found or access denied"
            }

        updated_task = toggle_task_completion(session, UUID(task_id))

        if updated_task:
            return {
                "task_id": str(updated_task.id),
                "completed": updated_task.is_completed,
                "title": updated_task.title,
                "updated_at": updated_task.updated_at.isoformat()
            }
        else:
            return {
                "task_id": task_id,
                "completed": False,
                "status": "error",
                "message": "Failed to update task completion status"
            }