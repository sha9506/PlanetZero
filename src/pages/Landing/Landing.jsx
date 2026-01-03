import React from 'react';
import { Link } from 'react-router-dom';
import { FaGlobeAmericas, FaLeaf, FaChartLine, FaBell, FaTrophy, FaShieldAlt, FaUsers } from 'react-icons/fa';
import './Landing.css';

const Landing = () => {
  return (
    <div className="landing-page">
      {/* Top Navigation */}
      <nav className="landing-nav">
        <div className="landing-nav-container">
          <Link to="/" className="landing-logo">
            <FaGlobeAmericas className="logo-icon" />
            <span className="logo-text">PlanetZero</span>
          </Link>
          <div className="landing-nav-links">
            <Link to="/login" className="nav-link">Sign In</Link>
            <Link to="/signup" className="btn btn-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge"><FaLeaf style={{ marginRight: '8px' }} /> Earth, But Upgraded</div>
          <h1 className="hero-title">
            Your Journey to
            <span className="gradient-text"> Carbon Neutrality</span>
          </h1>
          <p className="hero-description">
            Track, analyze, and reduce your carbon footprint with intelligent insights 
            and personalized recommendations. Join the movement towards a sustainable future.
          </p>
          <div className="cta-buttons">
            <Link to="/signup" className="btn btn-primary btn-large">
              Start Your Journey
              <span>→</span>
            </Link>
            <Link to="/login" className="btn btn-secondary btn-large">
              Sign In
            </Link>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <div className="stat-value">10K+</div>
              <div className="stat-label">Active Users</div>
            </div>
            <div className="stat">
              <div className="stat-value">2M+</div>
              <div className="stat-label">Tons CO₂ Reduced</div>
            </div>
            <div className="stat">
              <div className="stat-value">98%</div>
              <div className="stat-label">Satisfaction Rate</div>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="floating-card card-1">
            <div className="card-icon"><FaGlobeAmericas /></div>
            <div className="card-text">Track Impact</div>
          </div>
          <div className="floating-card card-2">
            <div className="card-icon"><FaChartLine /></div>
            <div className="card-text">Analyze Data</div>
          </div>
          <div className="floating-card card-3">
            <div className="card-icon"><FaTrophy /></div>
            <div className="card-text">Achieve Goals</div>
          </div>
          <div className="floating-card card-4">
            <div className="card-icon"><FaLeaf /></div>
            <div className="card-text">Reduce Emissions</div>
          </div>
          <div className="floating-card card-5">
            <div className="card-icon"><FaUsers /></div>
            <div className="card-text">Join Community</div>
          </div>
          <div className="earth-globe"><FaGlobeAmericas /></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          {/* <span className="section-badge">Features</span> */}
          <h2 className="section-title">Everything You Need to <span className="gradient-text">Go Green</span></h2>
          <p className="section-description">
            Powerful tools and insights to help you make a real difference
          </p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon"><FaChartLine /></div>
            <h3 className="feature-title">Smart Tracking</h3>
            <p className="feature-description">
              Monitor your daily carbon footprint across transportation, energy consumption, 
              food choices, and lifestyle activities with precision.
            </p>
            <ul className="feature-list">
              <li>✓ Real-time emission calculations</li>
              <li>✓ Automatic activity logging</li>
              <li>✓ Multi-category tracking</li>
            </ul>
          </div>
          
          <div className="feature-card featured">
            <div className="featured-badge">Most Popular</div>
            <div className="feature-icon"><FaBell /></div>
            <h3 className="feature-title">AI Recommendations</h3>
            <p className="feature-description">
              Get personalized, actionable suggestions powered by AI to reduce your 
              environmental impact based on your unique lifestyle.
            </p>
            <ul className="feature-list">
              <li>✓ Personalized action plans</li>
              <li>✓ Impact predictions</li>
              <li>✓ Progress-based insights</li>
            </ul>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon"><FaChartLine /></div>
            <h3 className="feature-title">Visual Analytics</h3>
            <p className="feature-description">
              Beautiful, intuitive charts and graphs that make understanding your 
              environmental impact simple and engaging.
            </p>
            <ul className="feature-list">
              <li>✓ Interactive dashboards</li>
              <li>✓ Trend analysis</li>
              <li>✓ Goal tracking</li>
            </ul>
          </div>

          <div className="feature-card">
            <div className="feature-icon"><FaTrophy /></div>
            <h3 className="feature-title">Achievements</h3>
            <p className="feature-description">
              Stay motivated with milestones, badges, and achievements as you 
              progress on your sustainability journey.
            </p>
            <ul className="feature-list">
              <li>✓ Milestone rewards</li>
              <li>✓ Community challenges</li>
              <li>✓ Impact certificates</li>
            </ul>
          </div>

          <div className="feature-card">
            <div className="feature-icon"><FaLeaf /></div>
            <h3 className="feature-title">Offset Programs</h3>
            <p className="feature-description">
              Contribute to verified carbon offset projects and tree planting 
              initiatives around the world.
            </p>
            <ul className="feature-list">
              <li>✓ Verified projects</li>
              <li>✓ Direct impact tracking</li>
              <li>✓ Transparent reporting</li>
            </ul>
          </div>

          <div className="feature-card">
            <div className="feature-icon"><FaUsers /></div>
            <h3 className="feature-title">Community</h3>
            <p className="feature-description">
              Connect with like-minded individuals, share tips, and inspire 
              each other to make a difference.
            </p>
            <ul className="feature-list">
              <li>✓ Social features</li>
              <li>✓ Group challenges</li>
              <li>✓ Knowledge sharing</li>
            </ul>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Make a Difference?</h2>
          <p className="cta-description">
            Join thousands of users already on their journey to carbon neutrality
          </p>
          <Link to="/signup" className="btn btn-primary btn-large">
            Get Started Free
            <span>→</span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <FaGlobeAmericas className="logo-icon" />
              <span className="logo-text">PlanetZero</span>
            </div>
            <p className="footer-tagline">Earth, But Upgraded</p>
          </div>
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <a href="#features">Features</a>
              <a href="#pricing">Pricing</a>
              <a href="#faq">FAQ</a>
            </div>
            <div className="footer-column">
              <h4>Company</h4>
              <a href="#about">About</a>
              <a href="#blog">Blog</a>
              <a href="#careers">Careers</a>
            </div>
            <div className="footer-column">
              <h4>Support</h4>
              <a href="#help">Help Center</a>
              <a href="#contact">Contact</a>
              <a href="#privacy">Privacy</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} PlanetZero. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
