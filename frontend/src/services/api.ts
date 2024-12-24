import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Account {
  username: string;
  name: string;
  location: string;
  country: string;
  followers_count: number;
  annual_posts: number;
  thread_count: number;
  category: string;
  verified: boolean;
  engagement_score: number;
  intensity_score: number;
  ai_rank: number;
}

export interface SearchResponse {
  accounts: Account[];
  total_count: number;
}

export interface DashboardStats {
  total_influencers: number;
  average_engagement: number;
  active_countries: number;
  category_distribution: Record<string, number>;
  engagement_trends: {
    labels: string[];
    data: number[];
  };
}

export const searchAccounts = async (params: {
  topic: string;
  country?: string;
  category?: string;
  min_followers?: number;
  min_engagement?: number;
  sort_by?: string;
  page?: number;
  limit?: number;
}): Promise<SearchResponse> => {
  const response = await api.get('/search', { params });
  return response.data;
};

export const getLeaderboard = async (
  category: string = 'all',
  sort_by: string = 'ai_rank',
  limit: number = 10
): Promise<Account[]> => {
  const response = await api.get(`/leaderboard/${category}`, {
    params: { sort_by, limit },
  });
  return response.data;
};

export const getDashboardStats = async (): Promise<DashboardStats> => {
  const response = await api.get('/dashboard/stats');
  return response.data;
};

export const getCountries = async (): Promise<string[]> => {
  const response = await api.get('/countries');
  return response.data;
};

export const getCategories = async (): Promise<string[]> => {
  const response = await api.get('/categories');
  return response.data;
}; 