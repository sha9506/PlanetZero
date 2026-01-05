import React, { useState } from 'react';
import { 
  FaLightbulb, 
  FaBus, 
  FaUtensils, 
  FaLeaf, 
  FaBolt, 
  FaStar,
  FaCheck,
  FaChartLine,
  FaTasks
} from 'react-icons/fa';
import './RecommendationCard.css';

const RecommendationCard = ({ title, description, impact, difficulty, category }) => {
  const [isCompleted, setIsCompleted] = useState(false);

  const getCategoryIcon = () => {
    switch (category) {
      case 'energy':
        return <FaBolt />;
      case 'transport':
        return <FaBus />;
      case 'food':
        return <FaUtensils />;
      case 'lifestyle':
        return <FaLeaf />;
      default:
        return <FaLightbulb />;
    }
  };

  const getImpactDetails = () => {
    switch (impact) {
      case 'high':
        return { text: 'High Impact', stars: 3 };
      case 'medium':
        return { text: 'Medium Impact', stars: 2 };
      case 'low':
        return { text: 'Low Impact', stars: 1 };
      default:
        return { text: 'Unknown', stars: 0 };
    }
  };

  const impactDetails = getImpactDetails();

  return (
    <div className={`recommendation-card ${isCompleted ? 'completed' : ''}`}>
      <div className="recommendation-card-header">
        <div className={`category-icon ${category}`}>
          {getCategoryIcon()}
        </div>
        <span className={`category-badge ${category}`}>
          {category.charAt(0).toUpperCase() + category.slice(1)}
        </span>
      </div>

      <h3 className="recommendation-title">{title}</h3>
      <p className="recommendation-description">{description}</p>

      <div className="recommendation-metrics">
        <div className="metric">
          <div className="metric-icon">
            <FaChartLine />
          </div>
          <div className="metric-content">
            <span className="metric-label">Impact</span>
            <div className={`impact-stars ${impact}`}>
              {[...Array(3)].map((_, index) => (
                <FaStar key={index} className={index < impactDetails.stars ? 'filled' : ''} />
              ))}
            </div>
          </div>
        </div>

        <div className="metric">
          <div className="metric-icon">
            <FaTasks />
          </div>
          <div className="metric-content">
            <span className="metric-label">Difficulty</span>
            <span className={`difficulty-value ${difficulty}`}>
              {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
            </span>
          </div>
        </div>
      </div>

      <button
        className={`complete-btn ${isCompleted ? 'completed' : ''}`}
        onClick={() => setIsCompleted(!isCompleted)}
      >
        <FaCheck />
        {isCompleted ? 'Completed' : 'Mark as Done'}
      </button>
    </div>
  );
};

export default RecommendationCard;
