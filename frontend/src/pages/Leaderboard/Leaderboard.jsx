import React, { useState } from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaTrophy, FaMedal, FaStar, FaArrowUp, FaArrowDown, FaArrowRight, FaLock, FaCheckCircle, FaUsers } from 'react-icons/fa';
import './Leaderboard.css';

// Mock leaderboard data
const mockLeaderboardData = [
  {
    rank: 1,
    name: 'EcoWarrior',
    points: 2450,
    emissions: 125,
    badges: ['Top Performer', 'Green Hero', 'Recycling Champion'],
    trend: 'up',
  },
  {
    rank: 2,
    name: 'GreenGuardian',
    points: 2380,
    emissions: 132,
    badges: ['Runner Up', 'Bike Master', 'Energy Saver'],
    trend: 'up',
  },
  {
    rank: 3,
    name: 'PlanetProtector',
    points: 2310,
    emissions: 138,
    badges: ['Top 3', 'Earth Lover', 'Plant-Based Pro'],
    trend: 'same',
  },
  {
    rank: 4,
    name: 'CarbonCrusher',
    points: 2240,
    emissions: 145,
    badges: ['Rising Star', 'Walker Elite'],
    trend: 'up',
  },
  {
    rank: 5,
    name: 'You (Test User)',
    points: 2180,
    emissions: 152,
    badges: ['Newcomer', 'Tracker'],
    trend: 'up',
    isCurrentUser: true,
  },
  {
    rank: 6,
    name: 'SustainableSam',
    points: 2120,
    emissions: 158,
    badges: ['Water Saver', 'Tree Hugger'],
    trend: 'down',
  },
  {
    rank: 7,
    name: 'EcoEnthusiast',
    points: 2050,
    emissions: 165,
    badges: ['Recycler'],
    trend: 'same',
  },
  {
    rank: 8,
    name: 'GreenDreamer',
    points: 1980,
    emissions: 172,
    badges: ['Beginner'],
    trend: 'up',
  },
];

// Mock achievements
const allBadges = [
  { id: 1, icon: <FaTrophy />, name: 'Top Performer', description: 'Rank #1 on leaderboard', earned: false, color: 'gold' },
  { id: 2, icon: <FaStar />, name: 'Green Hero', description: 'Reduce emissions by 50%', earned: false, color: 'green' },
  { id: 3, icon: <FaMedal />, name: 'Recycling Champion', description: 'Log 30 days of recycling', earned: false, color: 'blue' },
  { id: 4, icon: <FaTrophy />, name: 'Bike Master', description: 'Bike 100km total', earned: false, color: 'purple' },
  { id: 5, icon: <FaStar />, name: 'Energy Saver', description: 'Save 500 kWh', earned: false, color: 'orange' },
  { id: 6, icon: <FaCheckCircle />, name: 'Newcomer', description: 'Join PlanetZero', earned: true, color: 'teal' },
  { id: 7, icon: <FaMedal />, name: 'Tracker', description: 'Log 7 consecutive days', earned: true, color: 'pink' },
  { id: 8, icon: <FaStar />, name: 'Earth Lover', description: 'Complete onboarding', earned: true, color: 'indigo' },
  { id: 9, icon: <FaUsers />, name: 'Community Founder', description: 'Start your own community', earned: false, color: 'emerald' },
];

const Leaderboard = () => {
  const [activeTab, setActiveTab] = useState('leaderboard');
  const currentUser = mockLeaderboardData.find(user => user.isCurrentUser);
  const earnedBadges = allBadges.filter(badge => badge.earned);

  return (
    <div className="leaderboard-page">
      <Navbar />
      <main className="leaderboard-content">
        <header className="leaderboard-header">
          <h1>Leaderboard</h1>
          <p>Compete with others and earn badges</p>
        </header>

        {/* User Stats Card */}
        <section className="user-stats-card">
          <div className="stats-left">
            <div className="rank-badge">
              <span className="rank-number">#{currentUser.rank}</span>
              <span className="rank-label">Your Rank</span>
            </div>
            <div className="user-info">
              <h3>{currentUser.name}</h3>
              <p className="user-points"><FaStar style={{ marginRight: '4px' }} /> {currentUser.points} points</p>
            </div>
          </div>
          <div className="stats-right">
            <div className="stat-item">
              <span className="stat-label">Emissions</span>
              <span className="stat-value">{currentUser.emissions} kg CO₂</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Badges</span>
              <span className="stat-value">{earnedBadges.length}/{allBadges.length}</span>
            </div>
          </div>
        </section>

        {/* Tabs */}
        <div className="leaderboard-tabs">
          <button
            className={`tab ${activeTab === 'leaderboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('leaderboard')}
          >
            <FaTrophy style={{ marginRight: '8px' }} /> Rankings
          </button>
          <button
            className={`tab ${activeTab === 'badges' ? 'active' : ''}`}
            onClick={() => setActiveTab('badges')}
          >
            <FaMedal style={{ marginRight: '8px' }} /> Badges
          </button>
        </div>

        {/* Leaderboard Tab */}
        {activeTab === 'leaderboard' && (
          <section className="rankings-section">
            <div className="rankings-list">
              {mockLeaderboardData.map((user) => (
                <div
                  key={user.rank}
                  className={`ranking-card ${user.isCurrentUser ? 'current-user' : ''} ${user.rank <= 3 ? 'top-three' : ''}`}
                >
                  <div className="rank-column">
                    <span className="rank-number">{user.rank}</span>
                    {user.rank === 1 && <FaTrophy className="medal gold" />}
                    {user.rank === 2 && <FaTrophy className="medal silver" />}
                    {user.rank === 3 && <FaTrophy className="medal bronze" />}
                  </div>

                  <div className="user-column">
                    <h3>{user.name}</h3>
                    <div className="user-badges">
                      {user.badges.slice(0, 2).map((badge, index) => (
                        <span key={index} className="mini-badge"><FaMedal style={{ marginRight: '4px' }} />{badge}</span>
                      ))}
                      {user.badges.length > 2 && (
                        <span className="badge-count">+{user.badges.length - 2}</span>
                      )}
                    </div>
                  </div>

                  <div className="stats-column">
                    <div className="stat">
                      <span className="stat-label">Points</span>
                      <span className="stat-value"><FaStar style={{ marginRight: '4px' }} /> {user.points}</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Emissions</span>
                      <span className="stat-value">{user.emissions} kg</span>
                    </div>
                  </div>

                  <div className="trend-column">
                    {user.trend === 'up' && <FaArrowUp className="trend-up" />}
                    {user.trend === 'down' && <FaArrowDown className="trend-down" />}
                    {user.trend === 'same' && <FaArrowRight className="trend-same" />}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Badges Tab */}
        {activeTab === 'badges' && (
          <section className="badges-section">
            <div className="badges-grid">
              {allBadges.map((badge) => (
                <div
                  key={badge.id}
                  className={`badge-card ${badge.earned ? 'earned' : 'locked'} badge-${badge.color}`}
                >
                  <div className="badge-icon">{badge.icon}</div>
                  <h3>{badge.name}</h3>
                  <p>{badge.description}</p>
                  {badge.earned ? (
                    <span className="badge-status earned-status"><FaCheckCircle style={{ marginRight: '4px' }} /> Earned</span>
                  ) : (
                    <span className="badge-status locked-status"><FaLock style={{ marginRight: '4px' }} /> Locked</span>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Leaderboard;
