import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import EmissionCard from '../../components/EmissionCard';
import ChartCard from '../../components/ChartCard';
import { FaGlobeAmericas, FaCar, FaBolt, FaUtensils } from 'react-icons/fa';
import api from '../../services/api';
import './Dashboard.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Dashboard = () => {
  const location = useLocation();
  const [emissionData, setEmissionData] = useState({
    total: 0,
    transport: 0,
    energy: 0,
    food: 0,
  });
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
    fetchChartData();
  }, [location.key, location.state?.refresh]); // Re-fetch when location changes or refresh state changes

  const handleRefresh = () => {
    fetchDashboardData();
    fetchChartData();
  };

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Fetch dashboard summary from backend
      const data = await api.getDashboardSummary();
      
      console.log('Dashboard data:', data);
      
      setEmissionData({
        total: data.total_emissions || 0,
        transport: data.transport_emissions || 0,
        energy: data.electricity_emissions || 0,
        food: data.food_emissions || 0,
      });
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data');
      // Keep default zero values on error
    } finally {
      setLoading(false);
    }
  };

  const fetchChartData = async () => {
    try {
      // Fetch chart data from backend
      const data = await api.getCharts(30);
      console.log('Chart data:', data);
      console.log('Monthly trend isEmpty:', data.monthly_trend?.isEmpty);
      console.log('Category breakdown isEmpty:', data.category_breakdown?.isEmpty);
      setChartData(data);
    } catch (err) {
      console.error('Failed to fetch chart data:', err);
      // Charts will show placeholder if data is null
    }
  };

  return (
    <div className="dashboard-page">
      <Navbar />
      <main className="dashboard-content">
        <header className="dashboard-header">
          <h1>Dashboard</h1>
          <p>Welcome back! Here's your carbon footprint overview.</p>
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
            <p>Loading dashboard data...</p>
          </div>
        ) : (
          <>
            <section className="emission-cards">
              <EmissionCard
                title="Total Emissions"
                value={emissionData.total}
                unit="kg CO₂"
                icon={<FaGlobeAmericas />}
                trend={-5}
              />
              <EmissionCard
                title="Transport"
                value={emissionData.transport}
                unit="kg CO₂"
                icon={<FaCar />}
                trend={-3}
              />
              <EmissionCard
                title="Energy"
                value={emissionData.energy}
                unit="kg CO₂"
                icon={<FaBolt />}
                trend={-8}
              />
              <EmissionCard
                title="Food"
                value={emissionData.food}
                unit="kg CO₂"
                icon={<FaUtensils />}
                trend={2}
              />
            </section>

            <section className="charts-section">
              <ChartCard title="Monthly Emissions Trend">
                {chartData && chartData.monthly_trend ? (
                  !chartData.monthly_trend.isEmpty ? (
                    <div style={{ height: '300px', position: 'relative' }}>
                      <Line
                        data={chartData.monthly_trend.data}
                        options={{
                          ...chartData.monthly_trend.options,
                          maintainAspectRatio: false
                        }}
                      />
                    </div>
                  ) : (
                    <div className="chart-placeholder">
                      <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
                        📊 No emission data available yet.<br/>
                        Start logging your daily activities to see your trends!
                      </p>
                    </div>
                  )
                ) : (
                  <div className="chart-placeholder">
                    <p style={{ color: '#6b7280' }}>Loading chart...</p>
                  </div>
                )}
              </ChartCard>

              <ChartCard title="Emissions by Category">
                {chartData && chartData.category_breakdown ? (
                  !chartData.category_breakdown.isEmpty ? (
                    <div style={{ height: '300px', position: 'relative' }}>
                      <Doughnut
                        data={chartData.category_breakdown.data}
                        options={{
                          ...chartData.category_breakdown.options,
                          maintainAspectRatio: false
                        }}
                      />
                    </div>
                  ) : (
                    <div className="chart-placeholder">
                      <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
                        📊 No category data available yet.<br/>
                        Start logging your daily activities to see your breakdown!
                      </p>
                    </div>
                  )
                ) : (
                  <div className="chart-placeholder">
                    <p style={{ color: '#6b7280' }}>Loading chart...</p>
                  </div>
                )}
              </ChartCard>
            </section>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Dashboard;
