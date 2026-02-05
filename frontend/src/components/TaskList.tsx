'use client';

import { useState, useEffect } from 'react';
import { useAuth } from './AuthProvider';
import { getTasks, updateTask, deleteTask, toggleTaskCompletion } from '../lib/api';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  onTasksChange?: (tasks: Task[]) => void;
}

export default function TaskList({ onTasksChange }: TaskListProps = {}) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [togglingTaskId, setTogglingTaskId] = useState<number | null>(null);
  const { user } = useAuth(); // Use auth context

  useEffect(() => {
    fetchTasks();
  }, [user]); // Add user as dependency

  useEffect(() => {
    if (onTasksChange) {
      onTasksChange(tasks);
    }
  }, [tasks, onTasksChange]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get the user ID from auth context
      if (!user || !user.id) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      const response = await getTasks(user.id);
      // Handle response based on whether it's wrapped in a 'tasks' property
      if (response.tasks !== undefined) {
        setTasks(response.tasks || []);
      } else {
        // If not wrapped, assume it's the array directly
        setTasks(response || []);
      }
    } catch (err) {
      setError('Failed to load tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      setTogglingTaskId(taskId);

      // Get the user ID from auth context
      if (!user || !user.id) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      // Find the current task to get its current completion status
      const currentTask = tasks.find(task => task.id === taskId);
      if (!currentTask) {
        throw new Error('Task not found');
      }

      // Toggle the completion status
      const newCompletionStatus = !currentTask.is_completed;
      const response = await toggleTaskCompletion(user.id, taskId, newCompletionStatus);

      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId
          ? { ...task, is_completed: response.is_completed, updated_at: response.updated_at }
          : task
      ));
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    } finally {
      setTogglingTaskId(null);
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      setDeletingTaskId(taskId);

      // Get the user ID from auth context
      if (!user || !user.id) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      await deleteTask(user.id, taskId);

      // Remove the task from the local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
    } finally {
      setDeletingTaskId(null);
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div key={index} className="flex items-center justify-between px-4 py-4 rounded-lg bg-gray-100 animate-pulse">
            <div className="flex items-center">
              <div className="h-5 w-5 rounded bg-gray-300 mr-3"></div>
              <div className="h-4 bg-gray-300 rounded w-32"></div>
            </div>
            <div className="h-4 w-12 bg-gray-300 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return <div className="text-center py-4 text-red-500">{error}</div>;
  }

  return (
    <div className="mt-6">
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-gray-100">
            <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <p className="text-gray-600">
              Showing <span className="font-medium">{tasks.length}</span> task{tasks.length !== 1 ? 's' : ''}
            </p>
            <div className="flex space-x-4">
              <p className="text-sm text-gray-500">
                {tasks.filter(t => t.is_completed).length} completed
              </p>
              <p className="text-sm text-gray-500">
                {tasks.filter(t => !t.is_completed).length} pending
              </p>
            </div>
          </div>
          <ul className="space-y-3">
            {tasks.map((task) => (
              <li
                key={task.id}
                className={`flex items-start justify-between px-4 py-4 rounded-lg transition-all duration-200 ${
                  task.is_completed
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200'
                    : 'bg-white border border-gray-200 shadow-sm hover:shadow-md'
                }`}
              >
                <div className="flex items-start">
                  <input
                    type="checkbox"
                    checked={task.is_completed}
                    onChange={() => handleToggleComplete(task.id)}
                    disabled={togglingTaskId === task.id}
                    className={`h-5 w-5 mt-0.5 rounded focus:ring-indigo-500 ${
                      task.is_completed
                        ? 'text-green-600 bg-green-200'
                        : 'text-indigo-600'
                    } ${togglingTaskId === task.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                  />
                  <div className="ml-3 flex-1 min-w-0">
                    <span className={`text-base font-medium ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {task.title}
                    </span>
                    {task.description && (
                      <p className={`mt-1 text-sm ${task.is_completed ? 'text-gray-400' : 'text-gray-500'}`}>
                        {task.description}
                      </p>
                    )}
                    <div className="flex items-center mt-1 text-xs text-gray-400">
                      <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => handleDelete(task.id)}
                    disabled={deletingTaskId === task.id}
                    className={`inline-flex items-center px-3 py-1.5 text-sm font-medium rounded-md transition-colors duration-200 ${
                      deletingTaskId === task.id
                        ? 'text-gray-400 cursor-not-allowed'
                        : 'text-red-600 hover:text-red-900 hover:bg-red-50'
                    }`}
                  >
                    {deletingTaskId === task.id ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Deleting...
                      </>
                    ) : (
                      <>
                        <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Delete
                      </>
                    )}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}