import React, { useState } from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaCar, FaBolt, FaUtensils, FaPlus, FaTrash } from 'react-icons/fa';
import './DailyLog.css';

const DailyLog = () => {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [activities, setActivities] = useState({
    transport: [],
    energy: {
      electricity: '',
      heating: '',
    },
    food: {
      meals: [],
    },
    shopping: [],
  });

  // State for new activity forms
  const [showTransportForm, setShowTransportForm] = useState(false);
  const [showMealForm, setShowMealForm] = useState(false);
  
  const [newTransport, setNewTransport] = useState({
    mode: '',
    distance: '',
    description: '',
  });

  const [newMeal, setNewMeal] = useState({
    type: '',
    description: '',
    servings: 1,
  });

  const handleAddTransport = () => {
    setShowTransportForm(true);
  };

  const handleSaveTransport = () => {
    if (newTransport.mode && newTransport.distance) {
      setActivities({
        ...activities,
        transport: [...activities.transport, { ...newTransport }],
      });
      setNewTransport({ mode: '', distance: '', description: '' });
      setShowTransportForm(false);
    }
  };

  const handleCancelTransport = () => {
    setNewTransport({ mode: '', distance: '', description: '' });
    setShowTransportForm(false);
  };

  const handleRemoveTransport = (index) => {
    setActivities({
      ...activities,
      transport: activities.transport.filter((_, i) => i !== index),
    });
  };

  const handleAddMeal = () => {
    setShowMealForm(true);
  };

  const handleSaveMeal = () => {
    if (newMeal.type && newMeal.description) {
      setActivities({
        ...activities,
        food: {
          ...activities.food,
          meals: [...activities.food.meals, { ...newMeal }],
        },
      });
      setNewMeal({ type: '', description: '', servings: 1 });
      setShowMealForm(false);
    }
  };

  const handleCancelMeal = () => {
    setNewMeal({ type: '', description: '', servings: 1 });
    setShowMealForm(false);
  };

  const handleRemoveMeal = (index) => {
    setActivities({
      ...activities,
      food: {
        ...activities.food,
        meals: activities.food.meals.filter((_, i) => i !== index),
      },
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate that at least one activity is logged
    const hasTransport = activities.transport.length > 0;
    const hasEnergy = activities.energy.electricity || activities.energy.heating;
    const hasMeals = activities.food.meals.length > 0;
    
    if (!hasTransport && !hasEnergy && !hasMeals) {
      alert('Please log at least one activity before saving.');
      return;
    }
    
    // Calculate estimated carbon footprint (simplified calculation)
    let totalCarbonKg = 0;
    
    // Transportation emissions (rough estimates in kg CO2)
    activities.transport.forEach(trip => {
      const distance = parseFloat(trip.distance) || 0;
      let emissionFactor = 0;
      
      switch(trip.mode) {
        case 'Car (Gasoline)': emissionFactor = 0.21; break;
        case 'Car (Diesel)': emissionFactor = 0.17; break;
        case 'Car (Electric)': emissionFactor = 0.05; break;
        case 'Car (Hybrid)': emissionFactor = 0.11; break;
        case 'Bus': emissionFactor = 0.08; break;
        case 'Train': emissionFactor = 0.04; break;
        case 'Subway/Metro': emissionFactor = 0.03; break;
        case 'Motorcycle': emissionFactor = 0.12; break;
        case 'Flight': emissionFactor = 0.25; break;
        default: emissionFactor = 0; // Bicycle, Walking
      }
      
      totalCarbonKg += distance * emissionFactor;
    });
    
    // Energy emissions (0.5 kg CO2 per kWh average)
    const electricityKwh = parseFloat(activities.energy.electricity) || 0;
    const heatingKwh = parseFloat(activities.energy.heating) || 0;
    totalCarbonKg += (electricityKwh + heatingKwh) * 0.5;
    
    // Meal emissions (rough estimates in kg CO2 per serving)
    activities.food.meals.forEach(meal => {
      const servings = parseInt(meal.servings) || 1;
      // Average estimate: 2 kg CO2 per meal
      totalCarbonKg += servings * 2;
    });
    
    const dailyLogData = {
      date,
      activities,
      carbonFootprint: totalCarbonKg.toFixed(2),
      timestamp: new Date().toISOString(),
    };
    
    // TODO: Submit to API endpoint
    console.log('Saving daily log:', dailyLogData);
    
    // Show success message
    alert(`Daily log saved successfully!\n\nEstimated carbon footprint: ${totalCarbonKg.toFixed(2)} kg CO2\n\nActivities logged:\n- Transportation: ${activities.transport.length} trips\n- Energy usage: ${electricityKwh + heatingKwh} kWh\n- Meals: ${activities.food.meals.length} meals`);
    
    // Optional: Reset form or redirect to dashboard
    // You can uncomment the line below to reset the form after saving
    // setActivities({ transport: [], energy: { electricity: '', heating: '' }, food: { meals: [] }, shopping: [] });
  };

  return (
    <div className="daily-log-page">
      <Navbar />
      <main className="daily-log-content">
        <header className="daily-log-header">
          <h1>Daily Log</h1>
          <p>Track your daily activities and their carbon impact</p>
        </header>

        <form onSubmit={handleSubmit} className="daily-log-form">
          <div className="form-group">
            <label htmlFor="date">Date</label>
            <input
              type="date"
              id="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <section className="log-section">
            <h2><FaCar /> Transportation</h2>
            <div className="activities-list">
              {activities.transport.length === 0 ? (
                <p className="empty-state">No transportation activities logged</p>
              ) : (
                activities.transport.map((activity, index) => (
                  <div key={index} className="activity-item">
                    <div className="activity-details">
                      <strong>{activity.mode}</strong> - {activity.distance} km
                      {activity.description && <p className="activity-desc">{activity.description}</p>}
                    </div>
                    <button 
                      type="button" 
                      onClick={() => handleRemoveTransport(index)}
                      className="btn-remove"
                      aria-label="Remove activity"
                    >
                      <FaTrash />
                    </button>
                  </div>
                ))
              )}
            </div>

            {showTransportForm && (
              <div className="activity-form">
                <div className="form-group">
                  <label htmlFor="transportMode">Transport Mode</label>
                  <select
                    id="transportMode"
                    value={newTransport.mode}
                    onChange={(e) => setNewTransport({ ...newTransport, mode: e.target.value })}
                  >
                    <option value="">Select mode...</option>
                    <option value="Car (Gasoline)">Car (Gasoline)</option>
                    <option value="Car (Diesel)">Car (Diesel)</option>
                    <option value="Car (Electric)">Car (Electric)</option>
                    <option value="Car (Hybrid)">Car (Hybrid)</option>
                    <option value="Bus">Bus</option>
                    <option value="Train">Train</option>
                    <option value="Subway/Metro">Subway/Metro</option>
                    <option value="Bicycle">Bicycle</option>
                    <option value="Walking">Walking</option>
                    <option value="Motorcycle">Motorcycle</option>
                    <option value="Flight">Flight</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="transportDistance">Distance (km)</label>
                  <input
                    type="number"
                    id="transportDistance"
                    value={newTransport.distance}
                    onChange={(e) => setNewTransport({ ...newTransport, distance: e.target.value })}
                    placeholder="0"
                    min="0"
                    step="0.1"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="transportDescription">Description (Optional)</label>
                  <input
                    type="text"
                    id="transportDescription"
                    value={newTransport.description}
                    onChange={(e) => setNewTransport({ ...newTransport, description: e.target.value })}
                    placeholder="e.g., Commute to work"
                  />
                </div>
                <div className="form-buttons">
                  <button type="button" onClick={handleSaveTransport} className="btn btn-primary btn-sm">
                    Save
                  </button>
                  <button type="button" onClick={handleCancelTransport} className="btn btn-secondary btn-sm">
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {!showTransportForm && (
              <button type="button" onClick={handleAddTransport} className="btn btn-secondary">
                <FaPlus /> Add Transportation
              </button>
            )}
          </section>

          <section className="log-section">
            <h2><FaBolt /> Energy Usage</h2>
            <div className="form-group">
              <label htmlFor="electricity">Electricity (kWh)</label>
              <input
                type="number"
                id="electricity"
                value={activities.energy.electricity}
                onChange={(e) =>
                  setActivities({
                    ...activities,
                    energy: { ...activities.energy, electricity: e.target.value },
                  })
                }
                placeholder="0"
                min="0"
                step="0.1"
              />
            </div>
            <div className="form-group">
              <label htmlFor="heating">Heating/Cooling (kWh)</label>
              <input
                type="number"
                id="heating"
                value={activities.energy.heating}
                onChange={(e) =>
                  setActivities({
                    ...activities,
                    energy: { ...activities.energy, heating: e.target.value },
                  })
                }
                placeholder="0"
                min="0"
                step="0.1"
              />
            </div>
          </section>

          <section className="log-section">
            <h2><FaUtensils /> Food & Diet</h2>
            <div className="activities-list">
              {activities.food.meals.length === 0 ? (
                <p className="empty-state">No meals logged</p>
              ) : (
                activities.food.meals.map((meal, index) => (
                  <div key={index} className="activity-item">
                    <div className="activity-details">
                      <strong>{meal.type}</strong> - {meal.description}
                      <p className="activity-desc">Servings: {meal.servings}</p>
                    </div>
                    <button 
                      type="button" 
                      onClick={() => handleRemoveMeal(index)}
                      className="btn-remove"
                      aria-label="Remove meal"
                    >
                      <FaTrash />
                    </button>
                  </div>
                ))
              )}
            </div>

            {showMealForm && (
              <div className="activity-form">
                <div className="form-group">
                  <label htmlFor="mealType">Meal Type</label>
                  <select
                    id="mealType"
                    value={newMeal.type}
                    onChange={(e) => setNewMeal({ ...newMeal, type: e.target.value })}
                  >
                    <option value="">Select meal type...</option>
                    <option value="Breakfast">Breakfast</option>
                    <option value="Lunch">Lunch</option>
                    <option value="Dinner">Dinner</option>
                    <option value="Snack">Snack</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="mealDescription">Description</label>
                  <input
                    type="text"
                    id="mealDescription"
                    value={newMeal.description}
                    onChange={(e) => setNewMeal({ ...newMeal, description: e.target.value })}
                    placeholder="e.g., Chicken salad, Pasta with vegetables"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="mealServings">Servings</label>
                  <input
                    type="number"
                    id="mealServings"
                    value={newMeal.servings}
                    onChange={(e) => setNewMeal({ ...newMeal, servings: e.target.value })}
                    min="1"
                    max="10"
                  />
                </div>
                <div className="form-buttons">
                  <button type="button" onClick={handleSaveMeal} className="btn btn-primary btn-sm">
                    Save
                  </button>
                  <button type="button" onClick={handleCancelMeal} className="btn btn-secondary btn-sm">
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {!showMealForm && (
              <button type="button" onClick={handleAddMeal} className="btn btn-secondary">
                <FaPlus /> Add Meal
              </button>
            )}
          </section>

          <button type="submit" className="btn btn-primary">
            Save Daily Log
          </button>
        </form>
      </main>
      <Footer />
    </div>
  );
};

export default DailyLog;
