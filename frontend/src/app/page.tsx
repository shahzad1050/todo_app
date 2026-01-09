// This will be the main page - redirect to login if not authenticated, or to dashboard if authenticated
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { checkAuthStatus } from '../lib/auth';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const isAuthenticated = await checkAuthStatus();
      if (isAuthenticated) {
        router.push('/dashboard');
      } else {
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome to TaskMaster</h1>
        <p className="text-gray-600 mb-6">Your personal task management solution</p>
        <div className="inline-flex items-center text-indigo-600">
          <span>Redirecting...</span>
        </div>
      </div>
    </div>
  );
}