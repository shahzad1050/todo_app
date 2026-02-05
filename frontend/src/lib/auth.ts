// Authentication utility functions

// For GitHub Pages deployment, we need to call the backend directly
// Update this URL to point to your deployed backend server
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8005'; // Updated to point to integrated backend

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
    // Create a username from first and last name or use email as username
    const username = userData.firstName && userData.lastName
      ? `${userData.firstName.toLowerCase()}.${userData.lastName.toLowerCase()}`
      : userData.email.split('@')[0];

    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        first_name: userData.firstName || '',
        last_name: userData.lastName || '',
      }),
    });

    let result;
    const contentType = response.headers.get('content-type');

    if (contentType && contentType.includes('application/json')) {
      result = await response.json();
    } else {
      // Handle non-JSON responses (like HTML error pages)
      const text = await response.text();
      try {
        result = JSON.parse(text);
      } catch {
        // If response is not JSON, create a generic error object
        result = { detail: `Server error: ${response.status} ${response.statusText}` };
      }
    }

    if (response.ok) {
      // Store user info in localStorage (in a real app, you would also store the token)
      localStorage.setItem('user_id', result.id);
      localStorage.setItem('user_email', result.email);
      return { success: true, message: result.message, id: result.id, email: result.email };
    } else {
      return { success: false, message: result.detail || `Signup failed: ${response.status} ${response.statusText}` };
    }
  } catch (error: any) {
    console.error('Signup error:', error);
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return { success: false, message: 'Unable to connect to the server. Please make sure the backend is running and check your network connection.' };
    }
    return { success: false, message: 'Network error occurred during signup. Please check your connection and try again.' };
  }
};

// Login function
export const login = async (email: string, password: string): Promise<AuthResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    let result;
    const contentType = response.headers.get('content-type');

    if (contentType && contentType.includes('application/json')) {
      result = await response.json();
    } else {
      // Handle non-JSON responses (like HTML error pages)
      const text = await response.text();
      try {
        result = JSON.parse(text);
      } catch {
        // If response is not JSON, create a generic error object
        result = { detail: `Server error: ${response.status} ${response.statusText}` };
      }
    }

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
      return { success: false, message: result.detail || `Login failed: ${response.status} ${response.statusText}` };
    }
  } catch (error: any) {
    console.error('Login error:', error);
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return { success: false, message: 'Unable to connect to the server. Please make sure the backend is running and check your network connection.' };
    }
    return { success: false, message: 'Network error occurred during login. Please check your connection and try again.' };
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
  try {
    // In a real app, you would validate the token with the backend
    const userId = localStorage.getItem('user_id');
    console.log('userId:', userId);
    return !!userId; // Return true if user ID exists in localStorage
  } catch (error) {
    console.error('Error in checkAuthStatus:', error);
    return false;
  }
};