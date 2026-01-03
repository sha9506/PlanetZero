import React, { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import EmissionCard from '../../components/EmissionCard';
import ChartCard from '../../components/ChartCard';
import { FaGlobeAmericas, FaCar, FaBolt, FaUtensils } from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = () => {
  const [emissionData, setEmissionData] = useState({
    total: 0,
    transport: 0,
    energy: 0,
    food: 0,
  });

  useEffect(() => {
    // TODO: Fetch emission data from API
    setEmissionData({
      total: 245,
      transport: 120,
      energy: 85,
      food: 40,
    });
  }, []);

  return (
    <div className="dashboard-page">
      <Navbar />
      <main className="dashboard-content">
        <header className="dashboard-header">
          <h1>Dashboard</h1>
          <p>Welcome back! Here's your carbon footprint overview.</p>
        </header>

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
            <div className="chart-placeholder">
              {/* TODO: Add chart library (e.g., Chart.js, Recharts) */}
              <p>Chart visualization coming soon</p>
            </div>
          </ChartCard>

          <ChartCard title="Emissions by Category">
            <div className="chart-placeholder">
              {/* TODO: Add chart library */}
              <p>Chart visualization coming soon</p>
            </div>
          </ChartCard>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Dashboard;
