import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [stats, setStats] = useState({ total: 0, last_24h: 0 });

  useEffect(() => {
    fetch('http://localhost:8000/api/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.log('Error:', err));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1 style={{ color: '#dc3545', borderBottom: '2px solid #dc3545', paddingBottom: '10px' }}>
        ThreatView Dashboard
      </h1>
      
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
        <div style={{ 
          background: 'white', 
          padding: '20px', 
          borderRadius: '8px', 
          boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
          borderLeft: '4px solid #dc3545',
          flex: 1
        }}>
          <h3 style={{ margin: 0, color: '#666' }}>Total Threats</h3>
          <p style={{ fontSize: '32px', margin: '10px 0', fontWeight: 'bold' }}>{stats.total}</p>
        </div>
        
        <div style={{ 
          background: 'white', 
          padding: '20px', 
          borderRadius: '8px', 
          boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
          borderLeft: '4px solid #fd7e14',
          flex: 1
        }}>
          <h3 style={{ margin: 0, color: '#666' }}>Last 24 Hours</h3>
          <p style={{ fontSize: '32px', margin: '10px 0', fontWeight: 'bold' }}>{stats.last_24h}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;