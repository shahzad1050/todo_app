from typing import Dict, Any, List
from uuid import uuid4
from datetime import datetime

# Mock in-memory storage for tasks
mock_tasks_db = {}

def add_task_tool(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
    """
    Add a new task for a user (mock implementation)
    """
    task_id = str(uuid4())

    # Create a mock task
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    # Store in mock DB
    if user_id not in mock_tasks_db:
        mock_tasks_db[user_id] = {}
    mock_tasks_db[user_id][task_id] = task

    return {
        "task_id": task_id,
        "status": "added",
        "title": task["title"]
    }

def list_tasks_tool(user_id: str, status: str = "all") -> Dict[str, List[Dict[str, Any]]]:
    """
    List tasks for a user with optional status filter (mock implementation)
    """
    user_tasks = mock_tasks_db.get(user_id, {})

    # Filter by status if specified
    if status == "completed":
        filtered_tasks = [task for task in user_tasks.values() if task["completed"]]
    elif status == "pending":
        filtered_tasks = [task for task in user_tasks.values() if not task["completed"]]
    else:
        filtered_tasks = list(user_tasks.values())

    # Sort by creation date (newest first)
    filtered_tasks.sort(key=lambda x: x["created_at"], reverse=True)

    return {
        "tasks": filtered_tasks
    }

def update_task_tool(user_id: str, task_id: str, title: str = None, description: str = None) -> Dict[str, Any]:
    """
    Update an existing task (mock implementation)
    """
    user_tasks = mock_tasks_db.get(user_id, {})
    task = user_tasks.get(task_id)

    if not task:
        return {
            "task_id": task_id,
            "status": "error",
            "message": "Task not found or access denied"
        }

    # Update fields if provided
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    task["updated_at"] = datetime.utcnow().isoformat()

    return {
        "task_id": task_id,
        "title": task["title"],
        "description": task["description"],
        "updated_at": task["updated_at"]
    }

def delete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a task (mock implementation)
    """
    user_tasks = mock_tasks_db.get(user_id, {})
    task = user_tasks.get(task_id)

    if not task:
        return {
            "task_id": task_id,
            "status": "error",
            "message": "Task not found or access denied"
        }

    del user_tasks[task_id]

    return {
        "task_id": task_id,
        "status": "deleted",
        "title": task["title"]
    }

def complete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Mark a task as complete or incomplete (mock implementation)
    """
    user_tasks = mock_tasks_db.get(user_id, {})
    task = user_tasks.get(task_id)

    if not task:
        return {
            "task_id": task_id,
            "completed": False,
            "status": "error",
            "message": "Task not found or access denied"
        }

    # Toggle completion status
    task["completed"] = not task["completed"]
    task["updated_at"] = datetime.utcnow().isoformat()

    return {
        "task_id": task_id,
        "completed": task["completed"],
        "title": task["title"],
        "updated_at": task["updated_at"]
    }