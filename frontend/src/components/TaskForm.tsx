'use client';

import { useState } from 'react';
import { useAuth } from './AuthProvider';
import { createTask } from '@/lib/api';

interface TaskFormData {
  title: string;
  description: string;
}

export default function TaskForm() {
  const { user } = useAuth(); // Use auth context
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
      if (!user || !user.id) {
        setError('User not authenticated. Please log in first.');
        return;
      }

      const response = await createTask(user.id, {
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
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-1 shadow-lg">
      <div className="bg-white rounded-2xl p-6">
        <div className="flex items-center mb-6">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-2 rounded-lg mr-3">
            <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-800">
            Add New Task
          </h2>
        </div>

        {error && (
          <div className="rounded-lg bg-red-50 p-4 mb-6 border border-red-200 flex items-start">
            <svg className="h-5 w-5 text-red-400 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-1 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        )}

        {success && (
          <div className="rounded-lg bg-green-50 p-4 mb-6 border border-green-200 flex items-start">
            <svg className="h-5 w-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <h3 className="text-sm font-medium text-green-800">Success</h3>
              <div className="mt-1 text-sm text-green-700">
                <p>{success}</p>
              </div>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-800 mb-2 font-semibold">
              Task Title *
            </label>
            <div className="relative">
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                className={`w-full px-4 py-3 pl-10 pr-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200 ${
                  error && !formData.title.trim()
                    ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                    : 'border-gray-300'
                }`}
                placeholder="What needs to be done?"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
            {error && !formData.title.trim() && (
              <p className="mt-1 text-sm text-red-600">Task title is required</p>
            )}
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-800 mb-2 font-semibold">
              Description
            </label>
            <div className="relative">
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={3}
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
                placeholder="Add details about your task (optional)"
              ></textarea>
              <div className="absolute inset-y-0 top-3 left-0 pl-3 flex items-start pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                </svg>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg text-base font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 transform hover:-translate-y-0.5 hover:shadow-md disabled:opacity-75 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Adding Task...
              </>
            ) : (
              <>
                <svg className="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Add Task
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}