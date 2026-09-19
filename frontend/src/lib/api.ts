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
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/api/v1/login', { email, password }, { timeout: 10000 });
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user_email', email);
    }
    return response.data;
  },
  signup: async (email: string, password: string) => {
    const response = await apiClient.post('/api/v1/signup', { email, password }, { timeout: 10000 });
    return response.data;
  },
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_email');
    }
  },
  getEmail: () => (typeof window !== 'undefined' ? localStorage.getItem('user_email') : null),
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

  streamMessage: async (
    query: string,
    conversationHistory: Array<{role: string, content: string}> = [],
    strategy = 'none',
    onToken: (content: string) => void,
    onMetadata: (data: {request_id: string, sources: any[]}) => void,
    onDone: (data: {answer: string, confidence: number, latency_ms: number, request_id: string, guardrail_meta: any}) => void,
    onError: (error: string) => void
  ) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${typeof window !== 'undefined' ? localStorage.getItem('access_token') : ''}`,
      },
      body: JSON.stringify({
        query,
        conversation_history: conversationHistory,
        query_rewrite_strategy: strategy,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_email');
          window.location.href = '/login';
        }
        throw new Error('Session expired or unauthorized');
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    if (!response.body) {
      throw new Error('No response body');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop() || '';

      for (const eventText of events) {
        if (!eventText.trim()) continue;

        const lines = eventText.split('\n');
        let eventType = '';
        let eventData = '';

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            eventType = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            eventData = line.slice(6);
          }
        }

        if (eventType && eventData) {
          try {
            const data = JSON.parse(eventData);

            switch (eventType) {
              case 'metadata':
                onMetadata(data);
                break;
              case 'token':
                if (data.content) {
                  onToken(data.content);
                }
                break;
              case 'done':
                onDone(data);
                break;
              case 'error':
                onError(data.detail || 'An error occurred');
                break;
            }
          } catch (parseError) {
            console.error('Failed to parse SSE data:', parseError, eventData);
          }
        }
      }
    }
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