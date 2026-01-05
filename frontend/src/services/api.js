// API base URL - FastAPI backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    let errorMessage = 'API request failed';
    
    try {
      const errorData = await response.json();
      
      // Don't log expected 404 errors for daily logs
      const isExpected404 = response.status === 404 && errorData.detail?.includes('No log found');
      
      if (!isExpected404) {
        console.log('API Error data:', errorData);
        console.log('Error data type:', typeof errorData);
        console.log('Error data keys:', Object.keys(errorData));
      }
      
      // FastAPI validation errors come as {detail: [{loc, msg, type}]}
      if (errorData.detail && Array.isArray(errorData.detail)) {
        errorMessage = errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
      } else if (errorData.detail) {
        errorMessage = errorData.detail;
      } else if (errorData.message) {
        errorMessage = errorData.message;
      } else {
        errorMessage = JSON.stringify(errorData);
      }
      
      if (!isExpected404) {
        console.log('Extracted error message:', errorMessage);
      }
    } catch (e) {
      console.error('Error parsing error response:', e);
      // If parsing fails, use status text
      errorMessage = response.statusText || errorMessage;
    }
    
    throw new Error(errorMessage);
  }
  return response.json();
};

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

// Helper function to get headers
const getHeaders = (includeAuth = true) => {
  const headers = {
    'Content-Type': 'application/json',
  };
  if (includeAuth) {
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return headers;
};

// API methods
const api = {
  // Authentication
  login: async (credentials) => {
    // Send JSON data matching backend LoginRequest schema
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });
    const data = await handleResponse(response);
    
    // Store token
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
    }
    
    return data;
  },

  signup: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: getHeaders(false),
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  logout: async () => {
    // Clear local storage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    return { message: 'Logged out successfully' };
  },

  // User Profile
  getProfile: async () => {
    const response = await fetch(`${API_BASE_URL}/profile`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  updateProfile: async (profileData) => {
    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(profileData),
    });
    return handleResponse(response);
  },

  completeOnboarding: async (onboardingData) => {
    // For now, update profile with onboarding data
    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(onboardingData),
    });
    return handleResponse(response);
  },

  // Daily Logs / Activities
  createDailyLog: async (logData) => {
    const token = getAuthToken();
    console.log('Creating daily log with token:', token ? 'Token exists' : 'NO TOKEN!');
    
    const response = await fetch(`${API_BASE_URL}/daily-log`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(logData),
    });
    return handleResponse(response);
  },

  getDailyLogs: async (limit = 30) => {
    const response = await fetch(`${API_BASE_URL}/history?limit=${limit}`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getDailyLog: async (date) => {
    const response = await fetch(`${API_BASE_URL}/daily-log/${date}`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  updateDailyLog: async (logData) => {
    // Same as create - backend handles upsert based on date
    const token = getAuthToken();
    console.log('Updating daily log with token:', token ? 'Token exists' : 'NO TOKEN!');
    
    const response = await fetch(`${API_BASE_URL}/daily-log`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(logData),
    });
    return handleResponse(response);
  },

  deleteDailyLog: async (date) => {
    // Not implemented in new backend - would need to add
    throw new Error('Delete not implemented yet');
  },

  getActivityStats: async () => {
    const response = await fetch(`${API_BASE_URL}/dashboard`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getDashboardSummary: async () => {
    const response = await fetch(`${API_BASE_URL}/dashboard`, {
      headers: getHeaders(),
    });
    const data = await handleResponse(response);
    // Backend returns {today, weekly, monthly} - return monthly by default
    return data.monthly || data.today || data;
  },

  // Recommendations
  getRecommendations: async () => {
    const response = await fetch(`${API_BASE_URL}/recommendations`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getRecommendation: async (recommendationId) => {
    const response = await fetch(`${API_BASE_URL}/recommendations/${recommendationId}`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  completeRecommendation: async (recommendationId) => {
    const response = await fetch(`${API_BASE_URL}/recommendations/${recommendationId}/complete`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  uncompleteRecommendation: async (recommendationId) => {
    const response = await fetch(`${API_BASE_URL}/recommendations/${recommendationId}/uncomplete`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getCompletedRecommendations: async () => {
    const response = await fetch(`${API_BASE_URL}/recommendations/user/completed`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  // Communities
  getCommunities: async (category = null, search = null) => {
    // Not implemented in clean backend - return empty for now
    return [];
  },

  getMyCommunities: async () => {
    return [];
  },

  getCommunity: async (communityId) => {
    throw new Error('Communities not implemented yet');
  },

  createCommunity: async (communityData) => {
    throw new Error('Communities not implemented yet');
  },

  joinCommunity: async (communityId) => {
    throw new Error('Communities not implemented yet');
  },

  leaveCommunity: async (communityId) => {
    throw new Error('Communities not implemented yet');
  },

  getCommunityMembers: async (communityId) => {
    return [];
  },

  updateCommunityActivities: async (communityId, activities) => {
    throw new Error('Communities not implemented yet');
  },

  // Leaderboard
  getLeaderboard: async (period = 'monthly', limit = 50) => {
    const response = await fetch(`${API_BASE_URL}/leaderboard?period=${period}&limit=${limit}`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getUserRank: async (userId) => {
    // User rank is included in leaderboard response
    const response = await fetch(`${API_BASE_URL}/leaderboard`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getLeaderboardStats: async () => {
    const response = await fetch(`${API_BASE_URL}/leaderboard`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  // Notifications
  getNotifications: async (unreadOnly = false, limit = 50) => {
    // Not implemented in clean backend - return empty for now
    return [];
  },

  getUnreadCount: async () => {
    return { count: 0 };
  },

  markNotificationRead: async (notificationId) => {
    return { message: 'Not implemented' };
  },

  markAllNotificationsRead: async () => {
    return { message: 'Not implemented' };
  },

  deleteNotification: async (notificationId) => {
    return { message: 'Not implemented' };
  },

  // Consent
  submitConsent: async (consentData) => {
    const response = await fetch(`${API_BASE_URL}/consent`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(consentData),
    });
    return handleResponse(response);
  },

  getConsent: async () => {
    const response = await fetch(`${API_BASE_URL}/consent`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  // Analytics (for future dashboard charts)
  getAnalytics: async (timeRange = '30d') => {
    // TODO: Implement analytics endpoint in backend
    return {
      message: 'Analytics endpoint not yet implemented',
      timeRange
    };
  },

  // Charts
  getCharts: async (days = 30) => {
    const response = await fetch(`${API_BASE_URL}/charts?days=${days}`, {
      headers: getHeaders(),
    });
    return handleResponse(response);
  },
};

export default api;
