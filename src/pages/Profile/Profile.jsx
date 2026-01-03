import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    location: '',
    householdSize: 1,
    transportMode: '',
    dietType: '',
    energySource: '',
  });

  useEffect(() => {
    // TESTING MODE: Load dummy profile data
    setProfile({
      name: 'Test User',
      email: 'test@planetzero.com',
      location: 'San Francisco, USA',
      householdSize: 2,
      transportMode: 'public',
      dietType: 'vegetarian',
      energySource: 'mixed',
    });
  }, []);

  const handleChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TESTING MODE: Just log and disable editing
    console.log('Profile update (testing mode):', profile);
    setIsEditing(false);
  };

  const handleLogout = () => {
    // TESTING MODE: Simple navigation to landing page
    console.log('Logout (testing mode)');
    navigate('/');
  };

  return (
    <div className="profile-page">
      <Navbar />
      <main className="profile-content">
        <header className="profile-header">
          <h1>Profile</h1>
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="btn btn-secondary"
          >
            {isEditing ? 'Cancel' : 'Edit Profile'}
          </button>
        </header>

        <form onSubmit={handleSubmit} className="profile-form">
          <section className="profile-section">
            <h2>Personal Information</h2>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={profile.name}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={profile.email}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                name="location"
                value={profile.location}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
          </section>

          <section className="profile-section">
            <h2>Lifestyle Information</h2>
            <div className="form-group">
              <label htmlFor="householdSize">Household Size</label>
              <input
                type="number"
                id="householdSize"
                name="householdSize"
                value={profile.householdSize}
                onChange={handleChange}
                disabled={!isEditing}
                min="1"
              />
            </div>
            <div className="form-group">
              <label htmlFor="transportMode">Primary Transport Mode</label>
              <select
                id="transportMode"
                name="transportMode"
                value={profile.transportMode}
                onChange={handleChange}
                disabled={!isEditing}
              >
                <option value="car">Car</option>
                <option value="public">Public Transport</option>
                <option value="bike">Bike/Walk</option>
                <option value="mixed">Mixed</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="dietType">Diet Type</label>
              <select
                id="dietType"
                name="dietType"
                value={profile.dietType}
                onChange={handleChange}
                disabled={!isEditing}
              >
                <option value="omnivore">Omnivore</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="pescatarian">Pescatarian</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="energySource">Primary Energy Source</label>
              <select
                id="energySource"
                name="energySource"
                value={profile.energySource}
                onChange={handleChange}
                disabled={!isEditing}
              >
                <option value="renewable">Renewable</option>
                <option value="mixed">Mixed Grid</option>
                <option value="fossil">Fossil Fuels</option>
                <option value="unknown">Don't Know</option>
              </select>
            </div>
          </section>

          {isEditing && (
            <button type="submit" className="btn btn-primary">
              Save Changes
            </button>
          )}
        </form>

        <section className="profile-actions">
          <button onClick={handleLogout} className="btn btn-danger">
            Logout
          </button>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Profile;
