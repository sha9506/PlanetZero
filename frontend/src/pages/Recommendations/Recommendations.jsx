import React, { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import RecommendationCard from '../../components/RecommendationCard';
import './Recommendations.css';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // TODO: Fetch recommendations from API
    setRecommendations([
      {
        id: 1,
        title: 'Switch to LED Bulbs',
        description: 'Replace traditional incandescent bulbs with energy-efficient LED bulbs to reduce your energy consumption by up to 75%.',
        impact: 'high',
        difficulty: 'easy',
        category: 'energy',
      },
      {
        id: 2,
        title: 'Use Public Transportation',
        description: 'Take public transport instead of driving alone. This can reduce your transportation emissions by up to 45%.',
        impact: 'high',
        difficulty: 'medium',
        category: 'transport',
      },
      {
        id: 3,
        title: 'Reduce Meat Consumption',
        description: 'Try Meatless Mondays or reduce meat consumption to 2-3 times per week to lower your food-related emissions.',
        impact: 'medium',
        difficulty: 'medium',
        category: 'food',
      },
      {
        id: 4,
        title: 'Install Smart Thermostat',
        description: 'A smart thermostat can optimize your heating and cooling, reducing energy waste by up to 20%.',
        impact: 'high',
        difficulty: 'hard',
        category: 'energy',
      },
      {
        id: 5,
        title: 'Buy Local Produce',
        description: 'Choose locally sourced food to reduce transportation emissions from your groceries.',
        impact: 'low',
        difficulty: 'easy',
        category: 'food',
      },
    ]);
  }, []);

  const filteredRecommendations =
    filter === 'all'
      ? recommendations
      : recommendations.filter((rec) => rec.category === filter);

  return (
    <div className="recommendations-page">
      <Navbar />
      <main className="recommendations-content">
        <header className="recommendations-header">
          <h1>Recommendations</h1>
          <p>Personalized suggestions to reduce your carbon footprint</p>
        </header>

        <div className="filter-section">
          <label>Filter by category:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Categories</option>
            <option value="energy">Energy</option>
            <option value="transport">Transport</option>
            <option value="food">Food</option>
            <option value="lifestyle">Lifestyle</option>
          </select>
        </div>

        <div className="recommendations-grid">
          {filteredRecommendations.map((rec) => (
            <RecommendationCard
              key={rec.id}
              title={rec.title}
              description={rec.description}
              impact={rec.impact}
              difficulty={rec.difficulty}
              category={rec.category}
            />
          ))}
        </div>

        {filteredRecommendations.length === 0 && (
          <p className="empty-state">No recommendations found for this category.</p>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Recommendations;
