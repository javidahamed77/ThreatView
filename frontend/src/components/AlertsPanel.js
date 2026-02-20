import React, { useState, useEffect } from 'react';

const AlertsPanel = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
    // Refresh every 30 seconds
    const interval = setInterval(fetchAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/alerts');
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAlertIcon = (type) => {
    switch(type) {
      case 'industry': return '🏥';
      case 'brand': return '🏢';
      default: return '📢';
    }
  };

  const getTimeAgo = (timestamp) => {
    const seconds = Math.floor((new Date() - new Date(timestamp)) / 1000);
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    return `${Math.floor(seconds / 86400)} days ago`;
  };

  if (loading) return <div style={{ padding: '20px', textAlign: 'center' }}>Loading alerts...</div>;

  return (
    <div style={{ 
      marginTop: '20px', 
      background: 'white', 
      padding: '20px', 
      borderRadius: '8px',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '5px' }}>
        <span>🚨</span> Active Alerts ({alerts.length})
      </h3>
      
      {alerts.length === 0 ? (
        <p style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
          No active alerts
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {alerts.map(alert => (
            <div key={alert.id} style={{
              padding: '12px',
              background: '#f8f9fa',
              borderRadius: '5px',
              borderLeft: `4px solid ${alert.type === 'industry' ? '#007bff' : '#fd7e14'}`
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span style={{ fontWeight: 'bold' }}>
                  {getAlertIcon(alert.type)} {alert.type === 'industry' ? 'Industry Alert' : 'Brand Alert'}
                </span>
                <span style={{ fontSize: '11px', color: '#666' }}>
                  {getTimeAgo(alert.created_at)}
                </span>
              </div>
              <p style={{ margin: 0, fontSize: '13px' }}>{alert.message}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AlertsPanel;