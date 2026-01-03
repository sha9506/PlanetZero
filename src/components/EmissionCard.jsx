import React from 'react';

const EmissionCard = ({ title, value, unit, icon, trend }) => {
  return (
    <div className="emission-card">
      <div className="emission-card-header">
        <span className="emission-icon">{icon}</span>
        <h3 className="emission-title">{title}</h3>
      </div>
      <div className="emission-card-body">
        <p className="emission-value">
          {value} <span className="emission-unit">{unit}</span>
        </p>
        {trend && (
          <span className={`emission-trend ${trend > 0 ? 'positive' : 'negative'}`}>
            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>
    </div>
  );
};

export default EmissionCard;
