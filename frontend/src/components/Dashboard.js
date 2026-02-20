import React, { useState, useEffect } from 'react';
import ThreatMap from './ThreatMap';
import MalwareTrends from './MalwareTrends';
import RecentIOCs from './RecentIOCs';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({ total: 0, last_24h: 0 });

  useEffect(() => {
    fetch('http://localhost:8000/api/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div className="dashboard">
      <h1>ThreatView Dashboard</h1>
      
      <div className="stats">
        <div className="stat-card">
          <h3>Total Threats</h3>
          <p>{stats.total}</p>
        </div>
        <div className="stat-card">
          <h3>Last 24 Hours</h3>
          <p>{stats.last_24h}</p>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="grid-item">
          <ThreatMap />
        </div>
        <div className="grid-item">
          <MalwareTrends />
        </div>
        <div className="grid-item full-width">
          <RecentIOCs />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;