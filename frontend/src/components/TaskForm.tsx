'use client';

import { useState, KeyboardEvent } from 'react';
import { createTask } from '../lib/api';

interface TaskFormData {
  title: string;
  description?: string;
}

export default function TaskForm() {
  const [formData, setFormData] = useState<TaskFormData>({ title: '', description: '' });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (error) setError(null);
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Validate required fields
    if (!formData.title.trim()) {
      setError('Task title is required');
      return;
    }

    setLoading(true);

    try {
      // Get the user ID from auth context
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      const response = await createTask(userId, {
        title: formData.title,
        description: formData.description
      });

      if (response.id) {
        setSuccess('Task created successfully!');
        setFormData({ title: '', description: '' });

        // In a real app, we would refresh the task list
        // For now, we'll just simulate a refresh after a delay
        setTimeout(() => {
          setSuccess(null);
        }, 3000);
      }
    } catch (err) {
      setError('Failed to create task. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-1 shadow-lg">
      <div className="bg-white rounded-2xl p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Add New Task
        </h2>
        {error && (
          <div className="rounded-lg bg-red-50 p-4 mb-4 border border-red-200">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-1 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}
        {success && (
          <div className="rounded-lg bg-green-50 p-4 mb-4 border border-green-200">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">Success</h3>
                <div className="mt-1 text-sm text-red-700">
                  <p>{success}</p>
                </div>
              </div>
            </div>
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-sm font-medium text-gray-800 mb-2 font-semibold">
              Task Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              required
              className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200 ${
                error && !formData.title.trim()
                  ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                  : 'border-gray-300'
              }`}
              placeholder="What needs to be done?"
            />
            {error && !formData.title.trim() && (
              <p className="mt-1 text-sm text-red-600">Task title is required</p>
            )}
          </div>
          <div className="mb-6">
            <label htmlFor="description" className="block text-sm font-medium text-gray-800 mb-2 font-semibold">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
              placeholder="Add details about your task (optional)"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg text-base font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 transform hover:-translate-y-0.5 hover:shadow-md disabled:opacity-75 disabled:cursor-not-allowed"
          >
            {loading ? 'Adding Task...' : 'Add Task'}
          </button>
        </form>
      </div>
    </div>
  );
}