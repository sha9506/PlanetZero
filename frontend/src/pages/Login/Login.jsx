import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showAuthMessage, setShowAuthMessage] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useUser();

  // Check if user was redirected here due to authentication requirement
  useEffect(() => {
    if (location.state?.from) {
      setShowAuthMessage(true);
      // Auto-hide message after 5 seconds
      const timer = setTimeout(() => setShowAuthMessage(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [location]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      console.log('Attempting login with:', formData.email);
      
      // Use the login function from UserContext
      const { profileData } = await login({
        email: formData.email,
        password: formData.password
      });
      
      console.log('Login successful, profile data:', profileData);
      
      // Determine where to navigate based on user's onboarding status
      let destination = '/dashboard'; // Default for returning users
      
      // Check if user has completed consent
      if (!profileData.has_consent) {
        destination = '/consent';
        console.log('User has no consent, redirecting to consent');
      } 
      // Check if user has completed onboarding
      else if (!profileData.onboarding_completed) {
        destination = '/onboarding';
        console.log('User has not completed onboarding, redirecting to onboarding');
      }
      
      console.log('Navigating to:', destination);
      navigate(destination, { replace: true });
      
    } catch (err) {
      console.error('Login error details:', err);
      console.error('Error type:', typeof err);
      console.error('Error message:', err.message);
      
      // Ensure we always have a string error message
      let errorMessage = 'Login failed. Please check your credentials.';
      
      if (err.message && typeof err.message === 'string') {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err.toString && err.toString() !== '[object Object]') {
        errorMessage = err.toString();
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Welcome Back</h1>
        <p className="subtitle">Sign in to your PlanetZero account</p>
        
        {showAuthMessage && (
          <div className="info-message" style={{
            padding: '1rem',
            marginBottom: '1.5rem',
            backgroundColor: '#fff3cd',
            border: '1px solid #ffc107',
            borderRadius: '8px',
            color: '#856404',
            textAlign: 'center'
          }}>
            ⚠️ Please sign in to continue
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
            />
          </div>

          {error && (
            <div className="error-message" style={{
              marginBottom: '1rem',
              animation: 'shake 0.3s ease-in-out'
            }}>
              ❌ {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={isLoading}>
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <p className="signup-link">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
