'use client';

import { useState, useEffect } from 'react';
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

  useEffect(() => {
    fetchTasks();
  }, []);

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
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      const response = await getTasks(userId);
      setTasks(response.tasks || []);
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
      const userId = localStorage.getItem('user_id');
      if (!userId) {
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
      const response = await toggleTaskCompletion(userId, taskId, newCompletionStatus);

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
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      await deleteTask(userId, taskId);

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
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <p className="text-gray-600">
              Showing <span className="font-medium">{tasks.length}</span> task{tasks.length !== 1 ? 's' : ''}
            </p>
            <p className="text-sm text-gray-500">
              {tasks.filter(t => t.is_completed).length} completed
            </p>
          </div>
          <ul className="space-y-3">
            {tasks.map((task) => (
              <li
                key={task.id}
                className={`flex items-start justify-between px-4 py-4 rounded-lg transition-all duration-200 ${
                  task.is_completed
                    ? 'bg-green-50 border border-green-200'
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
                    <p className="mt-1 text-xs text-gray-400">
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </p>
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
                    {deletingTaskId === task.id ? 'Deleting...' : 'Delete'}
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