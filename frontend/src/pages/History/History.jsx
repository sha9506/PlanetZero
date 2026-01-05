import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaChartBar, FaChartLine, FaTrophy, FaExclamationTriangle } from 'react-icons/fa';
import api from '../../services/api';
import './History.css';

const History = () => {
  const location = useLocation();
  const [historyData, setHistoryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistoryData();
  }, [location.key, location.state?.refresh]); // Re-fetch when location changes or refresh state changes

  const handleRefresh = () => {
    fetchHistoryData();
  };

  const fetchHistoryData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Fetch history from backend (last 30 days)
      const data = await api.getDailyLogs(30);
      
      console.log('History data:', data);
      
      // The backend returns {entries: [...], total_days: N}
      const logs = data.entries || [];
      
      // Transform backend data to frontend format
      const transformedData = logs.map(log => ({
        date: log.date,
        transport: log.transport_emissions || 0,
        energy: log.electricity_emissions || 0,
        food: log.food_emissions || 0,
        total: log.total_emissions || 0,
      }));
      
      setHistoryData(transformedData);
    } catch (err) {
      console.error('Failed to fetch history data:', err);
      setError('Failed to load history data');
    } finally {
      setLoading(false);
    }
  };

  // Calculate statistics
  const totalEmissions = historyData.reduce((sum, day) => sum + day.total, 0);
  const averageDaily = historyData.length > 0 ? Math.round(totalEmissions / historyData.length) : 0;
  const lowestDay = historyData.length > 0 
    ? historyData.reduce((min, day) => day.total < min.total ? day : min)
    : { total: 0, date: new Date().toISOString() };
  const highestDay = historyData.length > 0
    ? historyData.reduce((max, day) => day.total > max.total ? day : max)
    : { total: 0, date: new Date().toISOString() };

  return (
    <div className="history-page">
      <Navbar />
      <main className="history-content">
        <header className="history-header">
          <h1>Tracking History</h1>
          <p>View your carbon footprint over time</p>
          <button 
            onClick={handleRefresh}
            style={{
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#10b981',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '500'
            }}
          >
            🔄 Refresh Data
          </button>
        </header>

        {error && (
          <div className="error-message" style={{
            padding: '1rem',
            marginBottom: '1.5rem',
            backgroundColor: '#fee',
            border: '1px solid #fcc',
            borderRadius: '8px',
            color: '#c33',
            textAlign: 'center'
          }}>
            ❌ {error}
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <p>Loading history data...</p>
          </div>
        ) : historyData.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <p>No history data yet. Start logging your daily emissions!</p>
          </div>
        ) : (
          <>
            {/* Summary Cards */}
            <section className="history-summary">
          <div className="summary-card">
            <div className="summary-icon"><FaChartBar /></div>
            <div className="summary-info">
              <h3>Total Emissions</h3>
              <p className="summary-value">{totalEmissions.toFixed(2)} kg CO₂</p>
              <span className="summary-label">Last {historyData.length} days</span>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon"><FaChartLine /></div>
            <div className="summary-info">
              <h3>Daily Average</h3>
              <p className="summary-value">{averageDaily.toFixed(2)} kg CO₂</p>
              <span className="summary-label">Per day</span>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon"><FaTrophy /></div>
            <div className="summary-info">
              <h3>Best Day</h3>
              <p className="summary-value">{lowestDay.total.toFixed(2)} kg CO₂</p>
              <span className="summary-label">{new Date(lowestDay.date).toLocaleDateString()}</span>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon"><FaExclamationTriangle /></div>
            <div className="summary-info">
              <h3>Highest Day</h3>
              <p className="summary-value">{highestDay.total.toFixed(2)} kg CO₂</p>
              <span className="summary-label">{new Date(highestDay.date).toLocaleDateString()}</span>
            </div>
          </div>
        </section>

            {/* Chart Placeholder */}
            <section className="history-chart">
              <div className="chart-card">
                <h2>Emissions Trend</h2>
                <div className="chart-placeholder">
                  <div className="bar-chart">
                    {historyData.slice(0, 7).reverse().map((day, index) => (
                      <div key={index} className="bar-container">
                        <div 
                          className="bar" 
                          style={{ height: `${Math.min((day.total / 50) * 100, 100)}%` }}
                          title={`${day.total.toFixed(2)} kg CO₂`}
                        >
                          <span className="bar-value">{day.total.toFixed(1)}</span>
                        </div>
                        <span className="bar-label">
                          {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </section>

            {/* Detailed Table */}
            <section className="history-table">
              <div className="table-card">
                <h2>Daily Breakdown</h2>
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Transport</th>
                      <th>Energy</th>
                      <th>Food</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historyData.map((day, index) => (
                      <tr key={index}>
                        <td>{new Date(day.date).toLocaleDateString('en-US', { 
                          weekday: 'short',
                          year: 'numeric', 
                          month: 'short', 
                          day: 'numeric' 
                        })}</td>
                        <td>{day.transport.toFixed(2)} kg</td>
                        <td>{day.energy.toFixed(2)} kg</td>
                        <td>{day.food.toFixed(2)} kg</td>
                        <td className="total-cell"><strong>{day.total.toFixed(2)} kg</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default History;
