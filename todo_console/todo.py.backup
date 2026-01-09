"""
CLI Todo Application - Core Logic

This module contains the core data models and business logic for the todo application.
"""

class Task:
    """Represents a single todo task."""

    def __init__(self, task_id, title, description=None, completed=False):
        """
        Initialize a Task object.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task
            description (str, optional): Optional description of the task
            completed (bool): Whether the task is completed, defaults to False
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip() if description else None
        self.completed = completed

    def __repr__(self):
        """String representation of the Task object."""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def to_dict(self):
        """Convert the Task object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }


class TaskManager:
    """Manages a collection of tasks in memory."""

    def __init__(self):
        """Initialize the TaskManager with an empty task list and ID counter."""
        self.tasks = []  # List to store Task objects
        self.next_id = 1  # Counter for generating unique IDs

    def add_task(self, title, description=None):
        """
        Add a new task to the task list.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task

        Returns:
            Task: The newly created Task object
        """
        # Validate title
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        # Create new task with unique ID
        new_task = Task(self.next_id, title, description, completed=False)
        self.tasks.append(new_task)

        # Increment ID counter for next task
        self.next_id += 1

        return new_task

    def view_tasks(self):
        """
        Get all tasks in the task list.

        Returns:
            list: List of all Task objects
        """
        return self.tasks.copy()  # Return a copy to prevent external modification

    def get_task(self, task_id):
        """
        Get a specific task by ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task: The Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, description=None):
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If the task with the given ID doesn't exist
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        # Update title if provided
        if title is not None:
            if not isinstance(title, str) or not title.strip():
                raise ValueError("Task title must be a non-empty string")
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description.strip() if description else None

        return task

    def delete_task(self, task_id):
        """
        Delete a task by ID.

        Args:
            task_id (int): ID of the task to delete

        Raises:
            ValueError: If the task with the given ID doesn't exist
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        self.tasks.remove(task)

    def toggle_task_completion(self, task_id):
        """
        Toggle the completion status of a task.

        Args:
            task_id (int): ID of the task to update

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If the task with the given ID doesn't exist
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task.completed = not task.completed
        return task