import React, { useState, useEffect } from 'react';

const RecentIOCs = () => {
  const [threats, setThreats] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: 'last_seen', direction: 'desc' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchThreats();
  }, []);

  const fetchThreats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/threats');
      const data = await response.json();
      setThreats(data);
    } catch (error) {
      console.error('Error fetching threats:', error);
    } finally {
      setLoading(false);
    }
  };

  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedThreats = [...threats].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) {
      return sortConfig.direction === 'asc' ? -1 : 1;
    }
    if (a[sortConfig.key] > b[sortConfig.key]) {
      return sortConfig.direction === 'asc' ? 1 : -1;
    }
    return 0;
  });

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'critical': return '#dc3545';
      case 'high': return '#fd7e14';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getTypeStyle = (type) => {
    switch(type) {
      case 'ip': return { background: '#e3f2fd', color: '#1976d2' };
      case 'domain': return { background: '#f3e5f5', color: '#7b1fa2' };
      case 'url': return { background: '#e8f5e9', color: '#388e3c' };
      case 'hash': return { background: '#fff3e0', color: '#f57c00' };
      default: return { background: '#f5f5f5', color: '#666' };
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '20px' }}>Loading threats...</div>;
  }

  return (
    <div style={{ 
      marginTop: '30px', 
      background: 'white', 
      padding: '20px', 
      borderRadius: '8px',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ marginBottom: '20px', color: '#333' }}>
        📋 Recent Indicators of Compromise (IOCs)
      </h3>
      
      {threats.length === 0 ? (
        <p style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
          No threats found in database
        </p>
      ) : (
        <>
          <div style={{ marginBottom: '15px', color: '#666', fontSize: '14px' }}>
            Showing {sortedThreats.length} threats (click column headers to sort)
          </div>
          
          <table style={{ 
            width: '100%', 
            borderCollapse: 'collapse',
            fontSize: '14px'
          }}>
            <thead>
              <tr style={{ background: '#f8f9fa' }}>
                <th 
                  onClick={() => requestSort('indicator')} 
                  style={{ 
                    padding: '12px', 
                    cursor: 'pointer', 
                    textAlign: 'left',
                    borderBottom: '2px solid #dee2e6'
                  }}
                >
                  Indicator {sortConfig.key === 'indicator' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                </th>
                <th 
                  onClick={() => requestSort('type')} 
                  style={{ 
                    padding: '12px', 
                    cursor: 'pointer', 
                    textAlign: 'left',
                    borderBottom: '2px solid #dee2e6'
                  }}
                >
                  Type {sortConfig.key === 'type' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                </th>
                <th 
                  onClick={() => requestSort('source')} 
                  style={{ 
                    padding: '12px', 
                    cursor: 'pointer', 
                    textAlign: 'left',
                    borderBottom: '2px solid #dee2e6'
                  }}
                >
                  Source {sortConfig.key === 'source' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                </th>
                <th 
                  onClick={() => requestSort('severity')} 
                  style={{ 
                    padding: '12px', 
                    cursor: 'pointer', 
                    textAlign: 'left',
                    borderBottom: '2px solid #dee2e6'
                  }}
                >
                  Severity {sortConfig.key === 'severity' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                </th>
                <th 
                  onClick={() => requestSort('last_seen')} 
                  style={{ 
                    padding: '12px', 
                    cursor: 'pointer', 
                    textAlign: 'left',
                    borderBottom: '2px solid #dee2e6'
                  }}
                >
                  Last Seen {sortConfig.key === 'last_seen' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                </th>
              </tr>
            </thead>
            <tbody>
              {sortedThreats.slice(0, 15).map(threat => (
                <tr key={threat.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ 
                    padding: '12px', 
                    fontFamily: 'monospace',
                    fontSize: '13px'
                  }}>
                    {threat.indicator}
                  </td>
                  <td style={{ padding: '12px' }}>
                    <span style={{
                      ...getTypeStyle(threat.type),
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: '500'
                    }}>
                      {threat.type}
                    </span>
                  </td>
                  <td style={{ padding: '12px' }}>{threat.source}</td>
                  <td style={{ padding: '12px' }}>
                    <span style={{
                      color: getSeverityColor(threat.severity),
                      fontWeight: 'bold',
                      textTransform: 'uppercase',
                      fontSize: '12px'
                    }}>
                      {threat.severity}
                    </span>
                  </td>
                  <td style={{ 
                    padding: '12px', 
                    color: '#666', 
                    fontSize: '12px' 
                  }}>
                    {new Date(threat.last_seen).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
};

export default RecentIOCs;