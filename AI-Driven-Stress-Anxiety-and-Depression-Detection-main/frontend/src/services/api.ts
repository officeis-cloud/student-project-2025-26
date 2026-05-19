/**
 * API Configuration and Base Client
 */

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export interface ApiError {
  error: string;
  message?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  async request<T>(
    endpoint: string,
    options: Partial<{
      method: string;
      headers: Record<string, string>;
      body: string;
    }> = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || data.message || 'Request failed');
      }

      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  async get<T>(endpoint: string, options?: Record<string, any>): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  async post<T>(endpoint: string, body?: unknown, options?: Record<string, any>): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put<T>(endpoint: string, body?: unknown, options?: Record<string, any>): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete<T>(endpoint: string, options?: Record<string, any>): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);

// Token management
export const setAuthToken = (token: string) => {
  localStorage.setItem('access_token', token);
};

export const setRefreshToken = (token: string) => {
  localStorage.setItem('refresh_token', token);
};

export const getAuthToken = (): string | null => {
  return localStorage.getItem('access_token');
};

export const getRefreshToken = (): string | null => {
  return localStorage.getItem('refresh_token');
};

export const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const isAuthenticated = (): boolean => {
  return !!getAuthToken();
};

/**
 * Emotion Prediction API
 */
export interface EmotionPredictionRequest {
  text: string;
}

export interface EmotionPredictionResponse {
  success: boolean;
  entry_id: string;
  emotions: Record<string, number>;
  mental_state: string;
  severity: string;
  severity_score: number;
  state_scores: {
    depression: number;
    anxiety: number;
    stress: number;
  };
  recommendations: Array<{
    title: string;
    description: string;
    category: string;
  }>;
  timestamp: string;
}

export const predictEmotion = async (text: string): Promise<EmotionPredictionResponse> => {
  return apiClient.post<EmotionPredictionResponse>('/predict', { text });
};

// Journal/History endpoints
export interface JournalEntry {
  id: string;
  text: string;
  emotions: Record<string, number>;
  mental_state: string;
  severity: string;
  severity_score: number;
  recommendations: string[];
  created_at: string;
}

export interface HistoryResponse {
  success: boolean;
  entries: JournalEntry[];
  total: number;
  pages: number;
  current_page: number;
  per_page: number;
}

export const getJournalHistory = async (page: number = 1, per_page: number = 50): Promise<HistoryResponse> => {
  return apiClient.get<HistoryResponse>(`/predict/history?page=${page}&per_page=${per_page}`);
};

export const getJournalEntry = async (entryId: string): Promise<{ success: boolean; entry: JournalEntry }> => {
  return apiClient.get(`/predict/history/${entryId}`);
};

export const deleteJournalEntry = async (entryId: string): Promise<{ success: boolean; message: string }> => {
  return apiClient.delete(`/predict/history/${entryId}`);
};

// User Profile endpoints
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  age?: number;
  gender?: string;
  created_at: string;
}

export const getUserProfile = async (): Promise<{ user: UserProfile }> => {
  return apiClient.get('/user/profile');
};

export const updateUserProfile = async (data: Partial<Pick<UserProfile, 'name' | 'email' | 'age' | 'gender'>>): Promise<{ success: boolean; message: string; user: UserProfile }> => {
  return apiClient.put('/user/profile', data);
};

export const changePassword = async (currentPassword: string, newPassword: string): Promise<{ success: boolean; message: string }> => {
  return apiClient.post('/user/change-password', {
    currentPassword,
    newPassword
  });
};

export const deleteAccount = async (): Promise<{ success: boolean; message: string }> => {
  return apiClient.delete('/user/account');
};
