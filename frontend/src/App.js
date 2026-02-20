import React, { useState, useEffect } from 'react';
import ThreatMap from './components/ThreatMap';
import MalwareTrends from './components/MalwareTrends';
import RecentIOCs from './components/RecentIOCs';
import SearchIoC from './components/SearchIoC';
import AlertsPanel from './components/AlertsPanel';  // 👈 YEH LINE ADD KARO

function App() {
  const [stats, setStats] = useState({ total: 0, last_24h: 0 });

  useEffect(() => {
    fetch('http://localhost:8000/api/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif', 
      maxWidth: '1200px', 
      margin: '0 auto' 
    }}>
      <h1 style={{ 
        color: '#dc3545', 
        borderBottom: '2px solid #dc3545', 
        paddingBottom: '10px' 
      }}>
        ThreatView Dashboard
      </h1>
      
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
        <div style={{ 
          background: '#f8f9fa', 
          padding: '20px', 
          borderRadius: '5px', 
          flex: 1 
        }}>
          <h3 style={{ margin: 0, color: '#666' }}>Total Threats</h3>
          <p style={{ fontSize: '32px', margin: '10px 0', fontWeight: 'bold' }}>
            {stats.total}
          </p>
        </div>
        <div style={{ 
          background: '#f8f9fa', 
          padding: '20px', 
          borderRadius: '5px', 
          flex: 1 
        }}>
          <h3 style={{ margin: 0, color: '#666' }}>Last 24 Hours</h3>
          <p style={{ fontSize: '32px', margin: '10px 0', fontWeight: 'bold' }}>
            {stats.last_24h}
          </p>
        </div>
      </div>

      <SearchIoC />
      <AlertsPanel />  {/* 👈 YEH LINE ADD KARO */}
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        <ThreatMap />
        <MalwareTrends />
      </div>
      
      <RecentIOCs />
    </div>
  );
}

export default App;