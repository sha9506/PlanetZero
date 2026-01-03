import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { UserProvider, useUser } from './context/UserContext';
import './App.css';
import './pages-styles.css';

// Pages
import Intro from './pages/Intro/Intro';
import Landing from './pages/Landing/Landing';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';
import Consent from './pages/Consent/Consent';
import Onboarding from './pages/Onboarding/Onboarding';
import Dashboard from './pages/Dashboard/Dashboard';
import DailyLog from './pages/DailyLog/DailyLog';
import Recommendations from './pages/Recommendations/Recommendations';
import Profile from './pages/Profile/Profile';
import History from './pages/History/History';
import Leaderboard from './pages/Leaderboard/Leaderboard';
import Community from './pages/Community/Community';

// Protected Route Component
// TESTING MODE: Disabled authentication check
const ProtectedRoute = ({ children }) => {
  // TODO: Re-enable authentication when backend is ready
  // const { isAuthenticated, loading } = useUser();
  // if (loading) return <div className="loading">Loading...</div>;
  // return isAuthenticated ? children : <Navigate to="/login" replace />;
  
  return children; // Allow access without authentication for testing
};

// Public Route Component (redirects to dashboard if already authenticated)
// TESTING MODE: Disabled redirect for testing
const PublicRoute = ({ children }) => {
  // TODO: Re-enable authentication redirect when backend is ready
  // const { isAuthenticated, loading } = useUser();
  // if (loading) return <div className="loading">Loading...</div>;
  // return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
  
  return children; // Allow access for testing
};

function AppContent() {
  return (
    <Router>
      <Routes>
        {/* Intro Page - First page users see */}
        <Route path="/" element={<Intro />} />
        
        {/* Public Routes */}
        <Route path="/landing" element={<Landing />} />
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/signup"
          element={
            <PublicRoute>
              <Signup />
            </PublicRoute>
          }
        />
        
        {/* Onboarding Routes */}
        <Route path="/consent" element={<Consent />} />
        <Route path="/onboarding" element={<Onboarding />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/daily-log"
          element={
            <ProtectedRoute>
              <DailyLog />
            </ProtectedRoute>
          }
        />
        <Route
          path="/recommendations"
          element={
            <ProtectedRoute>
              <Recommendations />
            </ProtectedRoute>
          }
        />
        <Route
          path="/community"
          element={
            <ProtectedRoute>
              <Community />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          }
        />
        <Route
          path="/leaderboard"
          element={
            <ProtectedRoute>
              <Leaderboard />
            </ProtectedRoute>
          }
        />

        {/* Fallback Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <UserProvider>
      <AppContent />
    </UserProvider>
  );
}

export default App;
