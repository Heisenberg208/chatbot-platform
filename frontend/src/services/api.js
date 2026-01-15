import axios from 'axios';

const API_BASE_URL ="https://chatbot-platform-ps6i.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle authentication errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    return response.data;
  },

  async register(email, password) {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      email,
      password,
    });
    return response.data;
  },
};

export const projectService = {
  async getProjects() {
    const response = await api.get('/projects');
    return response.data;
  },

  async createProject(name, description) {
    const response = await api.post('/projects', { name, description });
    return response.data;
  },
};

export const promptService = {
  async getPrompts(projectId) {
    const response = await api.get(`/projects/${projectId}/prompts`);
    return response.data;
  },

  async addPrompt(projectId, content) {
    const response = await api.post(`/projects/${projectId}/prompts`, { content });
    return response.data;
  },
};

export const chatService = {
  async sendMessage(projectId, message, sessionId) {
    const response = await api.post('/chat', {
      project_id: projectId,
      message,
      session_id: sessionId,
    });
    return response.data;
  },
};

export default api;
