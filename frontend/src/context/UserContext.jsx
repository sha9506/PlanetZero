import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const UserContext = createContext();

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is authenticated on mount
  useEffect(() => {
    const initializeUser = async () => {
      const token = localStorage.getItem('authToken');
      if (token) {
        try {
          const profileData = await api.getProfile();
          // Store full profile data (includes user, has_consent, etc.)
          setUser(profileData);
        } catch (err) {
          console.error('Failed to fetch user profile:', err);
          localStorage.removeItem('authToken');
        }
      }
      setLoading(false);
    };

    initializeUser();
  }, []);

  const login = async (credentials) => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.login(credentials);
      // API returns {access_token, token_type}, token is already stored in api.login
      // Now fetch user profile (includes consent and onboarding status)
      const profileData = await api.getProfile();
      
      console.log('Profile data after login:', profileData);
      
      // Store full profile data (includes user, has_consent, etc.)
      setUser(profileData);
      
      return { 
        user: profileData.user, 
        token: response.access_token,
        profileData // Return full profile for navigation decisions
      };
    } catch (err) {
      console.error('UserContext login error:', err);
      console.error('Error stringified:', JSON.stringify(err, null, 2));
      console.error('Error keys:', Object.keys(err));
      
      // Extract error message and ensure we throw a proper Error instance
      let errorMessage = 'Login failed. Please try again.';
      
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.message) {
        errorMessage = String(err.message);
      } else if (err?.detail) {
        errorMessage = String(err.detail);
      }
      
      console.error('Extracted error message:', errorMessage);
      
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const signup = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      const newUser = await api.signup(userData);
      // After signup, login to get token
      await login({ email: userData.email, password: userData.password });
      return newUser;
    } catch (err) {
      console.error('UserContext signup error:', err);
      
      // Extract error message and ensure we throw a proper Error instance
      let errorMessage = 'Signup failed. Please try again.';
      
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.message) {
        errorMessage = err.message;
      } else if (err?.detail) {
        errorMessage = err.detail;
      }
      
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('authToken');
      setUser(null);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      setError(null);
      const updatedUserData = await api.updateProfile(profileData);
      // Profile update returns just the user object
      setUser(updatedUserData);
      return updatedUserData;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    signup,
    logout,
    updateProfile,
    isAuthenticated: !!user,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

export default UserContext;
