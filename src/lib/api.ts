import { auth } from './firebase';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

class ApiService {
  private async getAuthToken(): Promise<string | null> {
    const user = auth.currentUser;
    if (user) {
      try {
        const token = await user.getIdToken();
        return token;
      } catch (error) {
        console.error('Error getting auth token:', error);
        return null;
      }
    }
    return null;
  }

  private async makeRequest(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const token = await this.getAuthToken();
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        window.location.href = '/login';
        throw new Error('Authentication required');
      }
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response;
  }

  async getUserInfo() {
    const response = await this.makeRequest('/user');
    return response.json();
  }

  async analyzeReport(reportText: string, filename?: string) {
    const response = await this.makeRequest('/analyze', {
      method: 'POST',
      body: JSON.stringify({
        reportText,
        filename,
      }),
    });
    return response.json();
  }

  async analyzeFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const token = await this.getAuthToken();
    const headers: HeadersInit = {};
    
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/analyze/file`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Authentication required');
      }
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck() {
    const response = await this.makeRequest('/health');
    return response.json();
  }
}

export const apiService = new ApiService();
