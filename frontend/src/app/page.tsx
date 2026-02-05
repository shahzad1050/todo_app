'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/components/AuthProvider';

export default function Home() {
  const { user } = useAuth(); // Use auth context
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI Todo assistant. You can ask me to add, list, update, delete, or complete tasks using natural language. What would you like to do?", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [userId, setUserId] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('user_id') || user?.id || 'user123';
    }
    return user?.id || 'user123';
  });
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Update userId when user from auth context changes
  useEffect(() => {
    if (user && user.id) {
      setUserId(user.id);
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      const authToken = user?.id ? token : null; // Only use token if user is authenticated

      const response = await fetch(`/api/chat/${encodeURIComponent(userId)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken && { 'Authorization': `Bearer ${authToken}` }) // Only add Authorization header if token exists
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId || undefined
        })
      });

      // Check if response is ok before trying to parse JSON
      if (!response.ok) {
        if (response.status === 500) {
          throw new Error('Backend service is currently unavailable. Please make sure the backend server is running.');
        } else if (response.status === 404) {
          throw new Error('The chat service is not available. This might mean the backend API is not properly configured.');
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }

      let data;
      const contentType = response.headers.get('content-type');

      // Check if the response is JSON
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // If not JSON, try to parse as text and handle appropriately
        const text = await response.text();
        try {
          data = JSON.parse(text);
        } catch (e) {
          // If it's not valid JSON, return a generic error
          throw new Error('Invalid response format from server');
        }
      }

      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      const botMessage = {
        id: Date.now() + 1,
        text: data.response || "Sorry, I couldn't process that request.",
        sender: 'bot'
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);
      let errorMessageText = "Sorry, I encountered an error processing your request. Please try again.";

      if (error.message.includes('Backend service is currently unavailable')) {
        errorMessageText = "The AI assistant is currently unavailable. Please make sure the backend server is running and properly configured.";
      } else if (error.message.includes('chat service is not available')) {
        errorMessageText = "The chat service is not available. This might mean the backend API is not properly configured.";
      } else if (error.message.includes('NetworkError')) {
        errorMessageText = "Unable to connect to the server. Please check your network connection and make sure the backend is running.";
      }

      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickActions = [
    { text: "Add task buy groceries", icon: "🛒" },
    { text: "Show my tasks", icon: "📋" },
    { text: "Complete task 1", icon: "✅" },
    { text: "Delete task 2", icon: "🗑️" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-100">
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6 text-center">
            <div className="flex items-center justify-center mb-3">
              <div className="bg-white/20 p-2 rounded-full mr-3">
                <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h1 className="text-3xl font-bold">AI Todo Assistant</h1>
            </div>
            <p className="opacity-90 text-lg">Manage your tasks with natural language</p>
          </div>

          {/* Instructions */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200 p-4">
            <div className="flex flex-wrap gap-2 justify-center">
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  onClick={() => setInputValue(action.text)}
                  className="flex items-center text-sm bg-white hover:bg-gray-50 text-gray-700 px-3 py-2 rounded-lg border border-gray-200 transition-colors"
                >
                  <span className="mr-2">{action.icon}</span>
                  <span>{action.text}</span>
                </button>
              ))}
            </div>
          </div>

          {/* User ID Input */}
          <div className="p-4 bg-gray-50 border-b">
            <label htmlFor="userId" className="block text-sm font-medium text-gray-700 mb-2">
              {user ? `Authenticated as: ${user.email || user.id}` : 'User ID (use any random ID for testing):'}
            </label>
            <div className="relative">
              <input
                type="text"
                id="userId"
                value={userId}
                onChange={(e) => !user && setUserId(e.target.value)} // Only allow change if not authenticated
                placeholder={user ? "Logged in user ID" : "Enter your user ID (e.g., user123)"}
                disabled={!!user} // Disable if authenticated
                className={`w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 ${user ? 'bg-gray-100' : ''}`}
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Chat Container */}
          <div className="h-96 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                    message.sender === 'user'
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-br-md shadow-md'
                      : 'bg-white text-gray-800 rounded-bl-md border border-gray-200 shadow-sm'
                  }`}
                >
                  <div className="flex items-start">
                    {message.sender === 'bot' && (
                      <div className="mr-2 mt-0.5">
                        <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-1 rounded-full">
                          <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                          </svg>
                        </div>
                      </div>
                    )}
                    <div>
                      {message.text}
                    </div>
                    {message.sender === 'user' && (
                      <div className="ml-2 mt-0.5">
                        <div className="bg-white/20 p-1 rounded-full">
                          <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-800 rounded-2xl rounded-bl-md px-4 py-3 max-w-xs border border-gray-200 shadow-sm">
                  <div className="flex items-center">
                    <div className="mr-2">
                      <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-1 rounded-full">
                        <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce delay-75"></div>
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce delay-150"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="p-4 border-t bg-white">
            <div className="relative">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask me to manage your tasks..."
                disabled={isLoading}
                className="w-full px-4 py-3 pl-10 pr-12 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSubmit(e)}
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-2 rounded-full hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? (
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                )}
              </button>
            </div>
          </form>
        </div>

        <div className="mt-8 text-center text-gray-600">
          <p>Not a member? <a href="/signup" className="text-indigo-600 hover:text-indigo-500 font-medium">Sign up</a> to save your tasks and access them from anywhere.</p>
        </div>
      </main>
    </div>
  );
}