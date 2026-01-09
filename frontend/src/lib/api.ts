// API utility functions for interacting with the backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface TaskCreateData {
  title: string;
  description?: string;
}

interface TaskUpdateData {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

interface TaskCompletionData {
  is_completed: boolean;
}

// Get all tasks for a user
export const getTasks = async (userId: string) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/tasks`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
  }

  return await response.json();
};

// Create a new task
export const createTask = async (userId: string, taskData: TaskCreateData) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
  }

  return await response.json();
};

// Get a specific task
export const getTask = async (userId: string, taskId: number) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/tasks/${taskId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch task: ${response.status} ${response.statusText}`);
  }

  return await response.json();
};

// Update a task
export const updateTask = async (userId: string, taskId: number, taskData: TaskUpdateData) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
  }

  return await response.json();
};

// Delete a task
export const deleteTask = async (userId: string, taskId: number) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
  }

  return await response.json();
};

// Toggle task completion
export const toggleTaskCompletion = async (userId: string, taskId: number, isCompleted: boolean) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ is_completed: isCompleted }),
  });

  if (!response.ok) {
    throw new Error(`Failed to toggle task completion: ${response.status} ${response.statusText}`);
  }

  return await response.json();
};