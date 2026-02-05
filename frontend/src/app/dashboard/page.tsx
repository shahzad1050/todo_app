'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/AuthProvider';
import TaskList from '../../components/TaskList';
import TaskForm from '../../components/TaskForm';
import TodoChatbot from '@/components/TodoChatbot';

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
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [showWelcome, setShowWelcome] = useState(true);
  const router = useRouter();
  const { user, isAuthenticated, logout: authLogout } = useAuth(); // Use auth context

  useEffect(() => {
    // Check authentication status using the context
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    // Auto-hide welcome message after 5 seconds
    const timer = setTimeout(() => {
      setShowWelcome(false);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  const handleLogout = async () => {
    await authLogout(); // Use the logout from auth context
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
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Loading Dashboard</h1>
          <p className="text-gray-600">We're preparing your tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100 overflow-hidden">
      {/* Welcome Banner */}
      {showWelcome && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-full shadow-lg flex items-center space-x-3 animate-bounce">
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span>Welcome back, {user?.email?.split('@')[0] || 'User'}!</span>
            <button
              onClick={() => setShowWelcome(false)}
              className="text-white hover:text-gray-200"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className={`flex-1 flex overflow-hidden transition-all duration-300 ${isSidebarOpen ? 'md:mr-80' : ''}`}>
        <div className="flex flex-col flex-1 overflow-hidden">
          <header className="bg-white/80 backdrop-blur-sm shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center">
                  <div className="flex-shrink-0 flex items-center">
                    <div className="flex items-center space-x-2">
                      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-2 rounded-lg">
                        <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                      </div>
                      <h1 className="text-xl font-bold text-gray-900">TaskMaster</h1>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                    className="bg-white hover:bg-gray-50 text-gray-700 p-2 rounded-lg transition duration-200 shadow-sm hover:shadow-md flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 border border-gray-200"
                    title="Refresh tasks"
                    aria-label="Refresh tasks"
                  >
                    {isRefreshing ? (
                      <svg className="animate-spin h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    ) : (
                      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    )}
                  </button>

                  <div className="flex items-center space-x-3">
                    <div className="hidden md:flex flex-col items-end">
                      <span className="text-sm font-medium text-gray-900 truncate max-w-xs" title={user?.email || ''}>{user?.email}</span>
                      <span className="text-xs text-gray-500">Dashboard</span>
                    </div>

                    {/* User Avatar */}
                    <div className="relative">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                        {user?.email?.charAt(0)?.toUpperCase() || 'U'}
                      </div>
                    </div>

                    <button
                      onClick={handleLogout}
                      className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-4 py-2 rounded-lg transition duration-200 shadow-md hover:shadow-lg flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                      title="Logout"
                      aria-label="Logout"
                    >
                      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      <span>Logout</span>
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
                    <h2 className="text-2xl font-bold text-gray-900">Good day, {user?.email?.split('@')[0] || 'User'}!</h2>
                    <p className="text-gray-600 mt-1">Here's what's happening with your tasks today.</p>
                  </div>
                  <div className="flex items-center space-x-2 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg px-4 py-2 border border-indigo-200">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium text-indigo-700">{tasks.length} tasks</span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Main Content Area */}
                <div className="lg:col-span-8 space-y-6">
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
                        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-indigo-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
                            style={{ width: `${(tasks.filter(t => t.is_completed).length / tasks.length) * 100}%` }}
                          ></div>
                        </div>
                      )}
                    </div>

                    <TaskList onTasksChange={handleTasksChange} />
                  </div>
                </div>

                {/* Stats and Quick Tips */}
                <div className="lg:col-span-4 space-y-6">
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
                        <svg className="h-5 w-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span className="font-medium">Click the checkbox to mark tasks as completed</span>
                      </li>
                      <li className="flex items-start p-3 rounded-lg hover:bg-indigo-50 transition-colors duration-200 border border-transparent hover:border-indigo-100 cursor-pointer">
                        <svg className="h-5 w-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        <span className="font-medium">Use the delete button to remove tasks</span>
                      </li>
                      <li className="flex items-start p-3 rounded-lg hover:bg-indigo-50 transition-colors duration-200 border border-transparent hover:border-indigo-100 cursor-pointer">
                        <svg className="h-5 w-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        <span className="font-medium">Add detailed descriptions for better task management</span>
                      </li>
                    </ul>
                  </div>

                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Assistant</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Need help managing your tasks? Our AI assistant can help you add, update, and complete tasks using natural language.
                    </p>
                    <button
                      onClick={() => setIsSidebarOpen(true)}
                      className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center space-x-2"
                    >
                      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                      </svg>
                      <span>Open AI Assistant</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>

      {/* Chatbot Sidebar */}
      <div
        className={`absolute md:relative transform transition-all duration-300 ease-in-out ${
          isSidebarOpen ? 'translate-x-0 w-80' : 'translate-x-full w-0'
        } h-full bg-white border-l border-gray-200 shadow-lg flex flex-col z-10`}
      >
        <div className="p-4 border-b border-gray-200 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-1.5 rounded-lg">
              <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-lg font-semibold text-gray-900">AI Todo Assistant</h2>
          </div>
          <button
            onClick={() => setIsSidebarOpen(false)}
            className="md:hidden inline-flex items-center p-1 border border-transparent rounded-full text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          <TodoChatbot />
        </div>
      </div>

      {/* Toggle Button for Mobile */}
      {!isSidebarOpen && (
        <button
          onClick={() => setIsSidebarOpen(true)}
          className="fixed bottom-6 right-6 md:hidden inline-flex items-center p-4 border border-transparent text-sm font-medium rounded-full shadow-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 z-10 transition-transform hover:scale-110"
        >
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </button>
      )}
    </div>
  );
}