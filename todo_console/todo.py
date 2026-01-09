"""
CLI Todo Application - Core Logic

This module contains the core data models and business logic for the todo application.
"""
import requests
import os

# Load environment variables from .env file if it exists
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    # .env file doesn't exist, that's okay
    pass


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
    """Manages a collection of tasks using the backend API."""

    def __init__(self, user_id=None, access_token=None):
        """Initialize the TaskManager with backend API connection."""
        # Get backend API URL from environment variable or use default
        self.api_base_url = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8001/api")

        # Handle authentication
        if user_id:
            self.user_id = user_id
        else:
            self.user_id = os.getenv("DEFAULT_USER_ID", "")

        if access_token:
            self.access_token = access_token
        else:
            self.access_token = os.getenv("ACCESS_TOKEN", "")

        # If no user ID is provided, we'll need to handle authentication
        if not self.user_id:
            print("No user ID provided. Please log in or sign up first.")
            # For now, we'll use a default user ID, but in a real app we'd implement auth flow
            self.user_id = "d5a81d40-7c96-4120-89c1-6616d145e7db"  # Default test user

    def _get_headers(self):
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def add_task(self, title, description=None):
        """
        Add a new task to the task list via API.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task

        Returns:
            Task: The newly created Task object
        """
        # Validate title
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        # Prepare data for API call
        task_data = {
            "title": title,
            "description": description
        }

        # Make API call to create task
        response = requests.post(
            f"{self.api_base_url}/users/{self.user_id}/tasks",
            json=task_data,
            headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to add task: {response.text}")

        # Parse response
        task_response = response.json()

        # Create and return Task object
        return Task(
            task_id=task_response['id'],
            title=task_response['title'],
            description=task_response['description'],
            completed=task_response['is_completed']
        )

    def view_tasks(self):
        """
        Get all tasks in the task list via API.

        Returns:
            list: List of all Task objects
        """
        # Make API call to get tasks
        response = requests.get(
            f"{self.api_base_url}/users/{self.user_id}/tasks",
            headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve tasks: {response.text}")

        # Parse response
        tasks_response = response.json()
        tasks_data = tasks_response.get('tasks', [])

        # Convert API response to Task objects
        tasks = []
        for task_data in tasks_data:
            task = Task(
                task_id=task_data['id'],
                title=task_data['title'],
                description=task_data['description'],
                completed=task_data['is_completed']
            )
            tasks.append(task)

        return tasks

    def get_task(self, task_id):
        """
        Get a specific task by ID via API.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task: The Task object if found, None otherwise
        """
        # Make API call to get specific task
        response = requests.get(
            f"{self.api_base_url}/users/{self.user_id}/tasks/{task_id}",
            headers=self._get_headers()
        )

        if response.status_code == 200:
            # Parse response
            task_data = response.json()
            return Task(
                task_id=task_data['id'],
                title=task_data['title'],
                description=task_data['description'],
                completed=task_data['is_completed']
            )
        else:
            return None

    def update_task(self, task_id, title=None, description=None):
        """
        Update an existing task via API.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If the task with the given ID doesn't exist
        """
        # Prepare data for API call
        update_data = {}
        if title is not None:
            if not isinstance(title, str) or not title.strip():
                raise ValueError("Task title must be a non-empty string")
            update_data["title"] = title.strip()
        if description is not None:
            update_data["description"] = description.strip() if description else None

        # Make API call to update task
        response = requests.put(
            f"{self.api_base_url}/users/{self.user_id}/tasks/{task_id}",
            json=update_data,
            headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to update task: {response.text}")

        # Parse response
        task_response = response.json()

        # Create and return updated Task object
        return Task(
            task_id=task_response['id'],
            title=task_response['title'],
            description=task_response['description'],
            completed=task_response['is_completed']
        )

    def delete_task(self, task_id):
        """
        Delete a task by ID via API.

        Args:
            task_id (int): ID of the task to delete

        Raises:
            ValueError: If the task with the given ID doesn't exist
        """
        # Make API call to delete task
        response = requests.delete(
            f"{self.api_base_url}/users/{self.user_id}/tasks/{task_id}",
            headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to delete task: {response.text}")

    def toggle_task_completion(self, task_id):
        """
        Toggle the completion status of a task via API.

        Args:
            task_id (int): ID of the task to update

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If the task with the given ID doesn't exist
        """
        # First, get the current task to determine its current completion status
        current_task = self.get_task(task_id)
        if not current_task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        # Toggle the completion status
        new_status = not current_task.completed

        # Make API call to update task completion
        response = requests.patch(
            f"{self.api_base_url}/users/{self.user_id}/tasks/{task_id}/complete",
            json={"is_completed": new_status},
            headers=self._get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to toggle task completion: {response.text}")

        # Parse response
        task_response = response.json()

        # Create and return updated Task object
        return Task(
            task_id=task_response['id'],
            title=task_response['title'],
            description=task_response['description'],
            completed=task_response['is_completed']
        )

    def login(self, email, password):
        """
        Authenticate user and get access token.

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            dict: User data including access token
        """
        login_data = {
            "email": email,
            "password": password
        }

        response = requests.post(
            f"{self.api_base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            user_data = response.json()
            self.user_id = user_data['id']
            self.access_token = user_data.get('access_token', '')
            return user_data
        else:
            raise Exception(f"Login failed: {response.text}")

    def signup(self, email, password, first_name=None, last_name=None):
        """
        Register a new user.

        Args:
            email (str): User's email
            password (str): User's password
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name

        Returns:
            dict: User data including access token
        """
        signup_data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }

        response = requests.post(
            f"{self.api_base_url}/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            user_data = response.json()
            self.user_id = user_data['id']
            self.access_token = user_data.get('access_token', '')
            return user_data
        else:
            raise Exception(f"Signup failed: {response.text}")