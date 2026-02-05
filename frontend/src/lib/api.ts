// API utility functions for interacting with the backend

// For GitHub Pages deployment, we need to call the backend directly
// Update this URL to point to your deployed backend server
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8005'; // Updated to point to integrated backend

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
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 500) {
        throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
      } else if (response.status === 404) {
        throw new Error('The tasks service is not available. This might mean the backend API is not properly configured.');
      } else {
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error: any) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to the server. Please make sure the backend is running and check your network connection.');
    }
    throw error;
  }
};

// Create a new task
export const createTask = async (userId: string, taskData: TaskCreateData) => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      if (response.status === 500) {
        throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
      } else if (response.status === 404) {
        throw new Error('The tasks service is not available. This might mean the backend API is not properly configured.');
      } else {
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error: any) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to the server. Please make sure the backend is running and check your network connection.');
    }
    throw error;
  }
};

// Get a specific task
export const getTask = async (userId: string, taskId: number) => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 500) {
        throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
      } else if (response.status === 404) {
        throw new Error('The task service is not available. This might mean the backend API is not properly configured.');
      } else {
        throw new Error(`Failed to fetch task: ${response.status} ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error: any) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to the server. Please make sure the backend is running and check your network connection.');
    }
    throw error;
  }
};

// Update a task
export const updateTask = async (userId: string, taskId: number, taskData: TaskUpdateData) => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      if (response.status === 500) {
        throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
      } else if (response.status === 404) {
        throw new Error('The task service is not available. This might mean the backend API is not properly configured.');
      } else {
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error: any) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to the server. Please make sure the backend is running and check your network connection.');
    }
    throw error;
  }
};

// Delete a task
export const deleteTask = async (userId: string, taskId: number) => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 500) {
        throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
      } else if (response.status === 404) {
        throw new Error('The task service is not available. This might mean the backend API is not properly configured.');
      } else {
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error: any) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to the server. Please make sure the backend is running and check your network connection.');
    }
    throw error;
  }
};

// Toggle task completion
export const toggleTaskCompletion = async (userId: string, taskId: number, isCompleted: boolean) => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ is_completed: isCompleted }),
    });

    if (!response.ok) {
      if (response.status === 500) {
        throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
      } else if (response.status === 404) {
        throw new Error('The task service is not available. This might mean the backend API is not properly configured.');
      } else {
        throw new Error(`Failed to toggle task completion: ${response.status} ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error: any) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to the server. Please make sure the backend is running and check your network connection.');
    }
    throw error;
  }
};