import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../services/api'; // Assuming api.js exports the configured axios instance

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
  const [loading, setLoading] = useState(true); // For initial check

  useEffect(() => {
    // Optional: Verify token with backend on initial load or refresh user details
    // For now, just assume token is valid if present, or decode it for user info
    const storedUser = localStorage.getItem('currentUser');
    if (accessToken && storedUser) {
      try {
        setCurrentUser(JSON.parse(storedUser));
      } catch (error) {
        console.error("Error parsing stored user data:", error);
        // Clear invalid stored data
        localStorage.removeItem('currentUser');
      }
    }
    setLoading(false);
  }, [accessToken]);

  const login = (userData, tokens) => {
    localStorage.setItem('accessToken', tokens.access);
    localStorage.setItem('refreshToken', tokens.refresh);
    localStorage.setItem('currentUser', JSON.stringify(userData)); // Store user object
    setAccessToken(tokens.access);
    setRefreshToken(tokens.refresh);
    setCurrentUser(userData);
    // apiClient's request interceptor will pick up the new token from localStorage
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('currentUser');
    setAccessToken(null);
    setRefreshToken(null);
    setCurrentUser(null);
    // apiClient's request interceptor will no longer find a token in localStorage
  };

  // Placeholder for register if it immediately logs in or just for consistency
  // const register = async (userData) => { /* call api, then potentially login */ };

  return (
    <AuthContext.Provider value={{ currentUser, accessToken, refreshToken, login, logout, isAuthenticated: !!accessToken, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
