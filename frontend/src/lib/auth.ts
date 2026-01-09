// Authentication utility functions

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface SignupData {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface AuthResponse {
  success: boolean;
  message: string;
  id?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  access_token?: string;
}

// Signup function
export const signup = async (userData: SignupData): Promise<AuthResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        first_name: userData.firstName,
        last_name: userData.lastName,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      // Store user info in localStorage (in a real app, you would also store the token)
      localStorage.setItem('user_id', result.id);
      localStorage.setItem('user_email', result.email);
      return { success: true, message: result.message, id: result.id, email: result.email };
    } else {
      return { success: false, message: result.detail || 'Signup failed' };
    }
  } catch (error) {
    console.error('Signup error:', error);
    return { success: false, message: 'Network error occurred during signup' };
  }
};

// Login function
export const login = async (email: string, password: string): Promise<AuthResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      // Store user info and token in localStorage
      localStorage.setItem('user_id', result.id);
      localStorage.setItem('user_email', result.email);
      if (result.access_token) {
        localStorage.setItem('token', result.access_token);
      }
      return {
        success: true,
        message: result.message,
        id: result.id,
        email: result.email,
        access_token: result.access_token
      };
    } else {
      return { success: false, message: result.detail || 'Login failed' };
    }
  } catch (error) {
    console.error('Login error:', error);
    return { success: false, message: 'Network error occurred during login' };
  }
};

// Logout function
export const logout = async (): Promise<boolean> => {
  try {
    // In a real app, you would call the logout endpoint
    // await fetch(`${API_BASE_URL}/api/auth/logout`, {
    //   method: 'POST',
    //   headers: {
    //     'Authorization': `Bearer ${localStorage.getItem('token')}`,
    //   },
    // });

    // Clear user data from localStorage
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('token');

    return true;
  } catch (error) {
    console.error('Logout error:', error);
    return false;
  }
};

// Check authentication status
export const checkAuthStatus = async (): Promise<boolean> => {
  // In a real app, you would validate the token with the backend
  const userId = localStorage.getItem('user_id');
  return !!userId; // Return true if user ID exists in localStorage
};