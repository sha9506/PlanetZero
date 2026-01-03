import React from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { FaChartBar, FaChartLine, FaTrophy, FaExclamationTriangle } from 'react-icons/fa';
import './History.css';

// Mock historical data
const mockHistoryData = [
  {
    date: '2025-12-19',
    transport: 45,
    energy: 32,
    food: 18,
    total: 95,
  },
  {
    date: '2025-12-18',
    transport: 52,
    energy: 28,
    food: 22,
    total: 102,
  },
  {
    date: '2025-12-17',
    transport: 38,
    energy: 35,
    food: 20,
    total: 93,
  },
  {
    date: '2025-12-16',
    transport: 48,
    energy: 30,
    food: 19,
    total: 97,
  },
  {
    date: '2025-12-15',
    transport: 55,
    energy: 33,
    food: 25,
    total: 113,
  },
  {
    date: '2025-12-14',
    transport: 42,
    energy: 29,
    food: 21,
    total: 92,
  },
  {
    date: '2025-12-13',
    transport: 40,
    energy: 31,
    food: 17,
    total: 88,
  },
];

const History = () => {
  const totalEmissions = mockHistoryData.reduce((sum, day) => sum + day.total, 0);
  const averageDaily = Math.round(totalEmissions / mockHistoryData.length);
  const lowestDay = mockHistoryData.reduce((min, day) => day.total < min.total ? day : min);
  const highestDay = mockHistoryData.reduce((max, day) => day.total > max.total ? day : max);

  return (
    <div className="history-page">
      <Navbar />
      <main className="history-content">
        <header className="history-header">
          <h1>Tracking History</h1>
          <p>View your carbon footprint over time</p>
        </header>

        {/* Summary Cards */}
        <section className="history-summary">
          <div className="summary-card">
            <div className="summary-icon"><FaChartBar /></div>
            <div className="summary-info">
              <h3>Total Emissions</h3>
              <p className="summary-value">{totalEmissions} kg CO₂</p>
              <span className="summary-label">Last 7 days</span>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon"><FaChartLine /></div>
            <div className="summary-info">
              <h3>Daily Average</h3>
              <p className="summary-value">{averageDaily} kg CO₂</p>
              <span className="summary-label">Per day</span>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon"><FaTrophy /></div>
            <div className="summary-info">
              <h3>Best Day</h3>
              <p className="summary-value">{lowestDay.total} kg CO₂</p>
              <span className="summary-label">{new Date(lowestDay.date).toLocaleDateString()}</span>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon"><FaExclamationTriangle /></div>
            <div className="summary-info">
              <h3>Highest Day</h3>
              <p className="summary-value">{highestDay.total} kg CO₂</p>
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
                {mockHistoryData.map((day, index) => (
                  <div key={index} className="bar-container">
                    <div 
                      className="bar" 
                      style={{ height: `${(day.total / 120) * 100}%` }}
                      title={`${day.total} kg CO₂`}
                    >
                      <span className="bar-value">{day.total}</span>
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
                {mockHistoryData.map((day, index) => (
                  <tr key={index}>
                    <td>{new Date(day.date).toLocaleDateString()}</td>
                    <td>{day.transport} kg</td>
                    <td>{day.energy} kg</td>
                    <td>{day.food} kg</td>
                    <td className="total-cell">{day.total} kg</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default History;
