'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { checkAuthStatus, logout } from '../../lib/auth';
import TaskList from '../../components/TaskList';
import TaskForm from '../../components/TaskForm';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const isAuthenticated = await checkAuthStatus();
      if (!isAuthenticated) {
        router.push('/login');
      } else {
        // In a real app, you would fetch user details here
        setUser({ email: 'user@example.com' });
      }
    };

    checkAuth();
  }, [router]);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    // In a real app, you would fetch fresh data here
    // For now, we'll just simulate a refresh
    setTimeout(() => {
      setIsRefreshing(false);
    }, 1000);
  };

  const handleTasksChange = (updatedTasks: Task[]) => {
    setTasks(updatedTasks);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-center">
            <p className="text-lg">Loading...</p>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Loading Dashboard</h1>
          <p className="text-gray-600">We're preparing your tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex">
      <div className="flex flex-col">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900">TaskMaster</h1>
                </div>
              </div>
              <div className="flex items-center">
                <button
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 p-2.5 rounded-full transition duration-200 shadow-sm hover:shadow-md flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50"
                  title="Refresh tasks"
                  aria-label="Refresh tasks"
                >
                  {isRefreshing ? 'Refreshing...' : 'Refresh'}
                </button>
                <div className="flex items-center space-x-3">
                  <div className="hidden md:flex flex-col items-end">
                    <span className="text-sm font-medium text-gray-900 truncate max-w-xs" title={user.email}>{user.email}</span>
                    <span className="text-xs text-gray-500">Dashboard</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white p-2.5 rounded-full transition duration-200 shadow-md hover:shadow-lg flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    title="Logout"
                    aria-label="Logout"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-4 sm:p-6">
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Good day, {user.email.split('@')[0]}!</h2>
                  <p className="text-gray-600 mt-1">Here's what's happening with your tasks today.</p>
                </div>
                <div className="flex items-center space-x-2 bg-indigo-50 rounded-lg px-4 py-2 border border-indigo-100">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium text-indigo-700">{tasks.length} tasks</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="md:col-span-2 lg:col-span-2 space-y-6">
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <TaskForm />
                </div>
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900" id="tasks-heading">Your Tasks</h3>
                      <p className="text-sm text-gray-500 mt-1" aria-describedby="tasks-heading">
                        {tasks.length > 0
                          ? `${tasks.filter(t => t.is_completed).length} of ${tasks.length} completed`
                          : 'No tasks yet'}
                      </p>
                    </div>
                  </div>
                  <div className="mb-6">
                    {tasks.length > 0 && (
                      <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-indigo-500 to-purple-600 h-2.5 rounded-full transition-all duration-1000 ease-out"
                          style={{ width: `${(tasks.filter(t => t.is_completed).length / tasks.length) * 100}%` }}
                        ></div>
                      </div>
                    )}
                  </div>
                  <TaskList onTasksChange={handleTasksChange} />
                </div>
              </div>
              <div className="md:col-span-2 lg:col-span-1 space-y-6">
                <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-6 text-white shadow-sm">
                  <h3 className="text-lg font-semibold mb-4">Dashboard Stats</h3>
                  <div className="space-y-4">
                    <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4 transition-all duration-300 hover:scale-[1.02] hover:bg-white/25 cursor-pointer">
                      <div className="flex items-center justify-between">
                        <p className="text-sm opacity-80">Total Tasks</p>
                      </div>
                      <p className="text-2xl font-bold mt-1">{tasks.length}</p>
                    </div>
                    <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4 transition-all duration-300 hover:scale-[1.02] hover:bg-white/25 cursor-pointer">
                      <div className="flex items-center justify-between">
                        <p className="text-sm opacity-80">Completed</p>
                      </div>
                      <p className="text-2xl font-bold mt-1">{tasks.filter(t => t.is_completed).length}</p>
                    </div>
                    <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4 transition-all duration-300 hover:scale-[1.02] hover:bg-white/25 cursor-pointer">
                      <div className="flex items-center justify-between">
                        <p className="text-sm opacity-80">Pending</p>
                      </div>
                      <p className="text-2xl font-bold mt-1">{tasks.filter(t => !t.is_completed).length}</p>
                    </div>
                  </div>
                </div>
                <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Quick Tips
                  </h3>
                  <ul className="space-y-3 text-sm text-gray-600">
                    <li className="flex items-start p-3 rounded-lg hover:bg-indigo-50 transition-colors duration-200 border border-transparent hover:border-indigo-100 cursor-pointer">
                      <span className="font-medium">Click the checkbox to mark tasks as completed</span>
                    </li>
                    <li className="flex items-start p-3 rounded-lg hover:bg-indigo-50 transition-colors duration-200 border border-transparent hover:border-indigo-100 cursor-pointer">
                      <span className="font-medium">Use the delete button to remove tasks</span>
                    </li>
                    <li className="flex items-start p-3 rounded-lg hover:bg-indigo-50 transition-colors duration-200 border border-transparent hover:border-indigo-100 cursor-pointer">
                      <span className="font-medium">Add detailed descriptions for better task management</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}