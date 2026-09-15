import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const authApi = {
  login: async (userId: string, roles: string[]) => {
    const response = await apiClient.post('/api/v1/token', { user_id: userId, roles }, { timeout: 10000 });
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user_id', userId);
      localStorage.setItem('user_roles', JSON.stringify(roles));
    }
    return response.data;
  },
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_roles');
    }
  },
  getUserId: () => (typeof window !== 'undefined' ? localStorage.getItem('user_id') : null),
  getRoles: () => (typeof window !== 'undefined' ? JSON.parse(localStorage.getItem('user_roles') || '[]') : []),
  isAuthenticated: () => (typeof window !== 'undefined' ? !!localStorage.getItem('access_token') : false),
};

export const chatApi = {
  sendMessage: async (query: string, conversationHistory: Array<{role: string, content: string}> = [], strategy = 'none') => {
    const response = await apiClient.post('/api/v1/chat', {
      query,
      conversation_history: conversationHistory,
      query_rewrite_strategy: strategy,
    });
    return response.data;
  },
};

export const ingestApi = {
  uploadFile: async (file: File, accessTags: string, piiFlags: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('access_tags', accessTags);
    formData.append('pii_flags', piiFlags);

    const response = await apiClient.post('/api/v1/ingest/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const healthApi = {
  check: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};