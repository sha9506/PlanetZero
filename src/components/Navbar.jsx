import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaGlobeAmericas, FaBell, FaTrophy, FaUsers, FaLeaf, FaCheckCircle, FaTimes } from 'react-icons/fa';
import './Navbar.css';

// Mock notifications data
const mockNotifications = [
  {
    id: 1,
    type: 'achievement',
    icon: <FaTrophy />,
    title: 'New Badge Earned!',
    message: 'Congratulations! You earned the "7-Day Streak" badge.',
    time: '2 hours ago',
    read: false,
  },
  {
    id: 2,
    type: 'community',
    icon: <FaUsers />,
    title: 'Community Update',
    message: 'Urban Gardeners has a new event: Community Garden Cleanup on Saturday.',
    time: '5 hours ago',
    read: false,
  },
  {
    id: 3,
    type: 'recommendation',
    icon: <FaLeaf />,
    title: 'New Recommendation',
    message: 'Based on your activity, we suggest trying composting to reduce waste.',
    time: '1 day ago',
    read: true,
  },
  {
    id: 4,
    type: 'milestone',
    icon: <FaCheckCircle />,
    title: 'Milestone Reached!',
    message: 'You\'ve saved 50kg of CO₂ this month! Keep up the great work.',
    time: '2 days ago',
    read: true,
  },
  {
    id: 5,
    type: 'community',
    icon: <FaUsers />,
    title: 'Community Invite',
    message: 'You\'ve been invited to join Zero Waste Warriors community.',
    time: '3 days ago',
    read: true,
  },
];

const Navbar = () => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState(mockNotifications);

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAsRead = (id) => {
    setNotifications(notifications.map(notif => 
      notif.id === id ? { ...notif, read: true } : notif
    ));
  };

  const markAllAsRead = () => {
    setNotifications(notifications.map(notif => ({ ...notif, read: true })));
  };

  const deleteNotification = (id) => {
    setNotifications(notifications.filter(notif => notif.id !== id));
  };

  const getNotificationColor = (type) => {
    switch(type) {
      case 'achievement': return '#fbbf24';
      case 'community': return '#14b8a6';
      case 'recommendation': return '#10b981';
      case 'milestone': return '#8b5cf6';
      default: return '#6b7280';
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <FaGlobeAmericas className="logo-icon" />
          <span className="logo-text">PlanetZero</span>
        </Link>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/dashboard" className="navbar-link">
              Dashboard
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/daily-log" className="navbar-link">
              Daily Log
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/history" className="navbar-link">
              History
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/recommendations" className="navbar-link">
              Recommendations
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/community" className="navbar-link">
              Community
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/leaderboard" className="navbar-link">
              Leaderboard
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/profile" className="navbar-link">
              Profile
            </Link>
          </li>
        </ul>
        
        {/* Notification Bell */}
        <div className="navbar-notifications">
          <button 
            className="notification-bell"
            onClick={() => setShowNotifications(!showNotifications)}
            aria-label="Notifications"
          >
            <FaBell />
            {unreadCount > 0 && (
              <span className="notification-badge">{unreadCount}</span>
            )}
          </button>

          {/* Notifications Dropdown */}
          {showNotifications && (
            <>
              <div 
                className="notification-overlay" 
                onClick={() => setShowNotifications(false)}
              />
              <div className="notifications-dropdown">
                <div className="notifications-header">
                  <h3>Notifications</h3>
                  {unreadCount > 0 && (
                    <button 
                      className="mark-all-read"
                      onClick={markAllAsRead}
                    >
                      Mark all as read
                    </button>
                  )}
                </div>

                <div className="notifications-list">
                  {notifications.length === 0 ? (
                    <div className="no-notifications">
                      <FaBell />
                      <p>No notifications yet</p>
                    </div>
                  ) : (
                    notifications.map((notification) => (
                      <div 
                        key={notification.id}
                        className={`notification-item ${notification.read ? 'read' : 'unread'}`}
                        onClick={() => markAsRead(notification.id)}
                      >
                        <div 
                          className="notification-icon"
                          style={{ backgroundColor: getNotificationColor(notification.type) }}
                        >
                          {notification.icon}
                        </div>
                        <div className="notification-content">
                          <h4>{notification.title}</h4>
                          <p>{notification.message}</p>
                          <span className="notification-time">{notification.time}</span>
                        </div>
                        <button 
                          className="delete-notification"
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteNotification(notification.id);
                          }}
                          aria-label="Delete notification"
                        >
                          <FaTimes />
                        </button>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
