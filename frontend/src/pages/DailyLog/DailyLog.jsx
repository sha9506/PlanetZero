import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import api from '../../services/api';
import { FaCar, FaBolt, FaUtensils, FaPlus, FaTrash } from 'react-icons/fa';
import './DailyLog.css';

const DailyLog = () => {
  const navigate = useNavigate();
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [todayLog, setTodayLog] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
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

  // Fetch today's log on component mount
  const fetchTodayLog = async () => {
    const today = new Date().toISOString().split('T')[0];
    try {
      const log = await api.getDailyLog(today);
      setTodayLog(log);
      
      // Parse backend data to frontend format for editing
      const parsedActivities = parseLogToActivities(log);
      setActivities(parsedActivities);
      setIsEditing(false); // Show view mode if log exists
    } catch (err) {
      // No log for today - that's expected, user can create one
      // Only log if it's not a 404 error
      if (!err.message.includes('No log found')) {
        console.error('Error fetching today\'s log:', err.message);
      }
      setTodayLog(null);
      setIsEditing(false); // Show form to create new log
    }
  };

  const parseLogToActivities = (log) => {
    // Convert backend format to frontend format
    const transport = log.transportation.map(t => {
      let mode = 'Car (Gasoline)';
      if (t.mode === 'car_petrol') mode = 'Car (Gasoline)';
      else if (t.mode === 'car_diesel') mode = 'Car (Diesel)';
      else if (t.mode === 'bus') mode = 'Bus';
      else if (t.mode === 'train') mode = 'Train';
      else if (t.mode === 'flight') mode = 'Flight';
      
      return {
        mode: mode,
        distance: String(t.distance_km),
        description: t.description || ''
      };
    });

    const meals = log.food.map(f => {
      let type = 'Breakfast'; // default
      if (f.meal_type === 'vegan') type = 'Vegan Meal';
      else if (f.meal_type === 'non_veg') type = 'Non-Veg Meal';
      else type = 'Veg Meal';
      
      return {
        type: type,
        description: f.description || type,
        servings: f.meals_count || 1
      };
    });

    const totalElectricity = log.electricity_kwh || 0;

    return {
      transport: transport,
      energy: {
        electricity: String(totalElectricity),
        heating: '0'
      },
      food: {
        meals: meals
      },
      shopping: []
    };
  };

  const handleEditLog = () => {
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    if (todayLog) {
      // Reset to original log data
      const parsedActivities = parseLogToActivities(todayLog);
      setActivities(parsedActivities);
    } else {
      // Reset to empty
      setActivities({
        transport: [],
        energy: { electricity: '', heating: '' },
        food: { meals: [] },
        shopping: []
      });
    }
    setIsEditing(false);
  };

  // Fetch today's log on component mount
  useEffect(() => {
    fetchTodayLog();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate that at least one activity is logged
    const hasTransport = activities.transport.length > 0;
    const hasEnergy = activities.energy.electricity || activities.energy.heating;
    const hasMeals = activities.food.meals.length > 0;
    
    if (!hasTransport && !hasEnergy && !hasMeals) {
      alert('Please log at least one activity before saving.');
      return;
    }
    
    try {
      setError(null);
      
      // Transform data to match backend API schema
      const transportationData = activities.transport.map(trip => {
        // Map frontend mode names to backend mode names
        let mode = 'car_petrol'; // default
        if (trip.mode.includes('Gasoline') || trip.mode.includes('Petrol')) mode = 'car_petrol';
        else if (trip.mode.includes('Diesel')) mode = 'car_diesel';
        else if (trip.mode.includes('Bus')) mode = 'bus';
        else if (trip.mode.includes('Train') || trip.mode.includes('Metro') || trip.mode.includes('Subway')) mode = 'train';
        else if (trip.mode.includes('Flight')) mode = 'flight';
        
        return {
          mode: mode,
          distance_km: parseFloat(trip.distance) || 0
        };
      });
      
      const electricityKwh = parseFloat(activities.energy.electricity) || 0;
      const heatingKwh = parseFloat(activities.energy.heating) || 0;
      const totalElectricity = electricityKwh + heatingKwh;
      
      // Transform meals to backend format
      const foodData = activities.food.meals.map(meal => {
        // Map meal types to backend types
        let meal_type = 'veg'; // default
        if (meal.type.toLowerCase().includes('vegan')) meal_type = 'vegan';
        else if (meal.type.toLowerCase().includes('non-veg') || 
                 meal.type.toLowerCase().includes('meat') ||
                 meal.type.toLowerCase().includes('chicken') ||
                 meal.type.toLowerCase().includes('fish')) meal_type = 'non_veg';
        else meal_type = 'veg';
        
        return {
          meal_type: meal_type,
          meals_count: parseInt(meal.servings) || 1
        };
      });
      
      // Submit to backend
      const logData = {
        date: date,
        transportation: transportationData,
        electricity_kwh: totalElectricity,
        food: foodData,
        lifestyle: [] // Not implemented in this form yet
      };
      
      console.log('Submitting daily log:', JSON.stringify(logData, null, 2));
      
      const response = await api.createDailyLog(logData);
      
      // Show success message
      const successMsg = `✅ Daily log ${todayLog ? 'updated' : 'saved'} successfully!\n\n📊 Total emissions: ${response.total_emissions.toFixed(2)} kg CO₂\n\nBreakdown:\n🚗 Transportation: ${response.transport_emissions.toFixed(2)} kg CO₂\n⚡ Electricity: ${response.electricity_emissions.toFixed(2)} kg CO₂\n🍽️ Food: ${response.food_emissions.toFixed(2)} kg CO₂`;
      
      setSuccessMessage(successMsg);
      setError(null);
      
      // Refresh today's log
      await fetchTodayLog();
      setIsEditing(false);
      
      // Redirect to dashboard with state to trigger refresh
      setTimeout(() => {
        navigate('/dashboard', { state: { refresh: Date.now() } });
      }, 3000);
      
    } catch (err) {
      console.error('Failed to save daily log:', err);
      setError(err.message || 'Failed to save daily log. Please make sure you have completed consent and onboarding first.');
      setSuccessMessage('');
    }
  };

  return (
    <div className="daily-log-page">
      <Navbar />
      <main className="daily-log-content">
        <header className="daily-log-header">
          <h1>Daily Log</h1>
          <p>Track your daily activities and their carbon impact</p>
        </header>

        {successMessage && (
          <div className="success-message" style={{
            padding: '1.5rem',
            marginBottom: '1.5rem',
            backgroundColor: '#d1fae5',
            border: '2px solid #10b981',
            borderRadius: '8px',
            color: '#065f46',
            whiteSpace: 'pre-line',
            fontWeight: '500'
          }}>
            {successMessage}
          </div>
        )}

        {error && (
          <div className="error-message" style={{
            padding: '1.5rem',
            marginBottom: '1.5rem',
            backgroundColor: '#fee2e2',
            border: '2px solid #ef4444',
            borderRadius: '8px',
            color: '#991b1b',
            fontWeight: '500'
          }}>
            ❌ {error}
          </div>
        )}

        {todayLog && !isEditing && (
          <section className="todays-entries">
            <div style={{
              backgroundColor: '#f0f9ff',
              border: '2px solid #3b82f6',
              borderRadius: '12px',
              padding: '1.5rem',
              marginBottom: '2rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ margin: 0, color: '#1e40af', fontSize: '1.5rem' }}>📋 Today's Entries</h2>
                <button 
                  type="button" 
                  onClick={handleEditLog}
                  className="btn btn-primary"
                  style={{ padding: '0.5rem 1rem' }}
                >
                  ✏️ Edit Entries
                </button>
              </div>

              <div style={{ display: 'grid', gap: '1.5rem' }}>
                {/* Summary */}
                <div style={{
                  backgroundColor: 'white',
                  padding: '1rem',
                  borderRadius: '8px',
                  border: '1px solid #bfdbfe'
                }}>
                  <h3 style={{ marginTop: 0, color: '#1e40af', fontSize: '1.1rem' }}>Total Emissions</h3>
                  <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#059669', margin: '0.5rem 0' }}>
                    {todayLog.total_emissions.toFixed(2)} kg CO₂
                  </p>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '0.5rem', marginTop: '1rem' }}>
                    <div>
                      <span style={{ color: '#6b7280' }}>🚗 Transport:</span> {todayLog.transport_emissions.toFixed(2)} kg
                    </div>
                    <div>
                      <span style={{ color: '#6b7280' }}>⚡ Energy:</span> {todayLog.electricity_emissions.toFixed(2)} kg
                    </div>
                    <div>
                      <span style={{ color: '#6b7280' }}>🍽️ Food:</span> {todayLog.food_emissions.toFixed(2)} kg
                    </div>
                  </div>
                </div>

                {/* Transportation Details */}
                {todayLog.transportation && todayLog.transportation.length > 0 && (
                  <div style={{
                    backgroundColor: 'white',
                    padding: '1rem',
                    borderRadius: '8px',
                    border: '1px solid #bfdbfe'
                  }}>
                    <h3 style={{ marginTop: 0, color: '#1e40af', fontSize: '1.1rem' }}>🚗 Transportation</h3>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                      {todayLog.transportation.map((trip, idx) => (
                        <li key={idx} style={{ padding: '0.5rem 0', borderBottom: idx < todayLog.transportation.length - 1 ? '1px solid #e5e7eb' : 'none' }}>
                          <strong>{trip.mode.replace('_', ' ').toUpperCase()}</strong> - {trip.distance_km} km
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Energy Details */}
                {todayLog.electricity_kwh > 0 && (
                  <div style={{
                    backgroundColor: 'white',
                    padding: '1rem',
                    borderRadius: '8px',
                    border: '1px solid #bfdbfe'
                  }}>
                    <h3 style={{ marginTop: 0, color: '#1e40af', fontSize: '1.1rem' }}>⚡ Energy Usage</h3>
                    <p style={{ margin: '0.5rem 0' }}>
                      Electricity: <strong>{todayLog.electricity_kwh} kWh</strong>
                    </p>
                  </div>
                )}

                {/* Food Details */}
                {todayLog.food && todayLog.food.length > 0 && (
                  <div style={{
                    backgroundColor: 'white',
                    padding: '1rem',
                    borderRadius: '8px',
                    border: '1px solid #bfdbfe'
                  }}>
                    <h3 style={{ marginTop: 0, color: '#1e40af', fontSize: '1.1rem' }}>🍽️ Food & Meals</h3>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                      {todayLog.food.map((meal, idx) => (
                        <li key={idx} style={{ padding: '0.5rem 0', borderBottom: idx < todayLog.food.length - 1 ? '1px solid #e5e7eb' : 'none' }}>
                          <strong>{meal.meal_type.replace('_', ' ').toUpperCase()}</strong> - {meal.meals_count} serving(s)
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {(isEditing || !todayLog) && (
          <form onSubmit={handleSubmit} className="daily-log-form">
          <div className="form-group">
            <label htmlFor="date">Date</label>
            <input
              type="date"
              id="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              max={new Date().toISOString().split('T')[0]}
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

          <div className="form-buttons" style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button type="submit" className="btn btn-primary">
              {todayLog ? 'Update Daily Log' : 'Save Daily Log'}
            </button>
            {todayLog && (
              <button type="button" onClick={handleCancelEdit} className="btn btn-secondary">
                Cancel
              </button>
            )}
          </div>
        </form>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default DailyLog;
