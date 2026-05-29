// API Configuration
// For local development, the Vite proxy will forward /api requests to the backend
// For production, update these URLs accordingly

// Use environment variable or detect if we're on mobile
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const backendHost = isLocalhost ? 'localhost' : window.location.hostname;

export const API_BASE_URL = import.meta.env.VITE_API_URL || `http://${backendHost}:8000`;

export const API_ENDPOINTS = {
  // Health & Status
  root: '/',
  health: '/api/system/health',
  stats: '/api/system/stats',
  
  // Chat
  chat: '/chat',
  chatStream: '/chat_stream',
  chatHistory: '/api/chat/history',
  
  // Avatar
  uploadAvatar: '/api/upload-avatar',
  
  // Scheduler
  scheduleAdd: '/api/schedule/add',
  scheduleAll: '/api/schedule/all',
  scheduleDelete: (id) => `/api/schedule/${id}`,
  notifications: '/api/notifications',
  
  // System
  systemExecute: '/api/system/execute',
};

// Helper function to get full URL
export const getApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  getApiUrl,
};
