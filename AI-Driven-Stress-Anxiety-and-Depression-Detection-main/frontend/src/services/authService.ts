/**
 * Authentication Service
 */

import { apiClient, setAuthToken, setRefreshToken, clearTokens } from './api';

export interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
  gender?: string;
  created_at?: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  age?: number;
  gender?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  access_token: string;
  refresh_token: string;
}

export interface ProfileUpdateData {
  name?: string;
  age?: number;
  gender?: string;
}

export interface PasswordChangeData {
  old_password: string;
  new_password: string;
}

class AuthService {
  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<AuthResponse>('/auth/register', data);
    
    // Store tokens
    setAuthToken(response.access_token);
    setRefreshToken(response.refresh_token);
    
    // Store user data
    localStorage.setItem('user', JSON.stringify(response.user));
    
    return response.user;
  }

  /**
   * Login user
   */
  async login(data: LoginData): Promise<User> {
    const response = await apiClient.post<AuthResponse>('/auth/login', data);
    
    // Store tokens
    setAuthToken(response.access_token);
    setRefreshToken(response.refresh_token);
    
    // Store user data
    localStorage.setItem('user', JSON.stringify(response.user));
    
    return response.user;
  }

  /**
   * Logout user
   */
  logout(): void {
    clearTokens();
    localStorage.removeItem('user');
  }

  /**
   * Get current user from localStorage
   */
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  /**
   * Fetch current user from API
   */
  async fetchCurrentUser(): Promise<User> {
    const response = await apiClient.get<{ user: User }>('/auth/me');
    
    // Update stored user data
    localStorage.setItem('user', JSON.stringify(response.user));
    
    return response.user;
  }

  /**
   * Update user profile
   */
  async updateProfile(data: ProfileUpdateData): Promise<User> {
    const response = await apiClient.put<{ message: string; user: User }>('/auth/profile', data);
    
    // Update stored user data
    localStorage.setItem('user', JSON.stringify(response.user));
    
    return response.user;
  }

  /**
   * Change password
   */
  async changePassword(data: PasswordChangeData): Promise<void> {
    await apiClient.post<{ message: string }>('/auth/change-password', data);
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<string> {
    const response = await apiClient.post<{ access_token: string }>('/auth/refresh');
    setAuthToken(response.access_token);
    return response.access_token;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }
}

export const authService = new AuthService();
