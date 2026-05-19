/**
 * Prediction and Mood Analysis Service
 */

import { apiClient } from './api';

export interface Emotion {
  [key: string]: number; // emotion name -> probability
}

export interface Recommendation {
  title: string;
  description: string;
  type: string;
  duration: string;
  icon: string;
  urgent?: boolean;
}

export interface MoodEntry {
  id: number;
  user_id: number;
  text: string;
  emotions: Emotion;
  mental_state: string;
  severity: string;
  severity_score: number;
  recommendations: string[];
  created_at: string;
}

export interface PredictionResult {
  success: boolean;
  entry_id: number;
  emotions: Emotion;
  mental_state: string;
  severity: string;
  severity_score: number;
  state_scores?: {
    depression: number;
    anxiety: number;
    stress: number;
  };
  recommendations: Recommendation[];
  timestamp: string;
}

export interface MoodHistoryResponse {
  success: boolean;
  entries: MoodEntry[];
  total: number;
  pages: number;
  current_page: number;
  per_page: number;
}

export interface MoodEntryDetail extends MoodEntry {
  full_recommendations: Recommendation[];
}

export interface MoodStatistics {
  success: boolean;
  total_entries: number;
  date_range: {
    start: string;
    end: string;
    days: number;
  };
  mental_state_distribution: {
    [state: string]: number;
  };
  severity_distribution: {
    [severity: string]: number;
  };
  average_severity_by_state: {
    [state: string]: number;
  };
  daily_data: {
    [date: string]: Array<{
      mental_state: string;
      severity: string;
      severity_score: number;
    }>;
  };
  most_common_state: string | null;
}

export interface RecommendationsResponse {
  success: boolean;
  mental_state: string;
  severity: string;
  severity_score: number;
  recommendations: Recommendation[];
  emergency_resources?: {
    crisis_helplines: Array<{
      name: string;
      number: string;
      description: string;
    }>;
    message: string;
  };
  last_updated?: string;
  message?: string;
}

export interface PredictTextData {
  text: string;
}

export interface QuickPredictionResult {
  success: boolean;
  emotions: Emotion;
}

class PredictionService {
  /**
   * Analyze text and get emotion prediction
   */
  async predictEmotion(text: string): Promise<PredictionResult> {
    return await apiClient.post<PredictionResult>('/predict/', { text });
  }

  /**
   * Quick emotion prediction without saving
   */
  async quickPredict(text: string): Promise<QuickPredictionResult> {
    return await apiClient.post<QuickPredictionResult>('/predict/quick', { text });
  }

  /**
   * Get mood entry history with pagination
   */
  async getMoodHistory(page: number = 1, perPage: number = 10): Promise<MoodHistoryResponse> {
    return await apiClient.get<MoodHistoryResponse>(
      `/predict/history?page=${page}&per_page=${perPage}`
    );
  }

  /**
   * Get detailed view of a specific mood entry
   */
  async getMoodDetail(entryId: number): Promise<MoodEntryDetail> {
    const response = await apiClient.get<{ success: boolean; entry: MoodEntryDetail }>(
      `/predict/history/${entryId}`
    );
    return response.entry;
  }

  /**
   * Delete a mood entry
   */
  async deleteMoodEntry(entryId: number): Promise<void> {
    await apiClient.delete(`/predict/history/${entryId}`);
  }

  /**
   * Get mood statistics
   */
  async getStatistics(days: number = 30): Promise<MoodStatistics> {
    return await apiClient.get<MoodStatistics>(`/predict/stats?days=${days}`);
  }

  /**
   * Get personalized recommendations
   */
  async getRecommendations(): Promise<RecommendationsResponse> {
    return await apiClient.get<RecommendationsResponse>('/predict/recommendations');
  }

  /**
   * Format emotion data for charts
   */
  formatEmotionsForChart(emotions: Emotion): Array<{ name: string; value: number }> {
    return Object.entries(emotions)
      .map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        value: Math.round(value * 100),
      }))
      .sort((a, b) => b.value - a.value);
  }

  /**
   * Get severity color
   */
  getSeverityColor(severity: string): string {
    const colors: { [key: string]: string } = {
      none: '#10b981',
      mild: '#fbbf24',
      moderate: '#f59e0b',
      severe: '#ef4444',
    };
    return colors[severity.toLowerCase()] || '#6b7280';
  }

  /**
   * Get mental state color
   */
  getMentalStateColor(state: string): string {
    const colors: { [key: string]: string } = {
      normal: '#10b981',
      stress: '#f59e0b',
      anxiety: '#8b5cf6',
      depression: '#3b82f6',
    };
    return colors[state.toLowerCase()] || '#6b7280';
  }

  /**
   * Get mental state emoji
   */
  getMentalStateEmoji(state: string): string {
    const emojis: { [key: string]: string } = {
      normal: '😊',
      stress: '😰',
      anxiety: '😟',
      depression: '😔',
    };
    return emojis[state.toLowerCase()] || '🙂';
  }
}

export const predictionService = new PredictionService();
