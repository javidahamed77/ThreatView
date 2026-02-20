import React, { useState } from 'react';

const SearchIoC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter an IP, domain, or URL');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`http://localhost:8000/api/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSearch();
  };

  return (
    <div style={{ 
      marginTop: '30px', 
      padding: '20px', 
      background: '#f8f9fa', 
      borderRadius: '5px' 
    }}>
      <h3>Search Indicators (IP / Domain / URL / Hash)</h3>
      
      <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
        <input
          type="text"
          placeholder="e.g., 192.168.1.1 or example.com"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          style={{
            flex: 1,
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px'
          }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{
            padding: '10px 20px',
            background: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div style={{ color: '#dc3545', marginTop: '10px' }}>{error}</div>
      )}

      {results && (
        <div style={{ marginTop: '20px' }}>
          <div style={{ 
            padding: '10px', 
            background: results.found ? '#d4edda' : '#fff3cd',
            borderRadius: '4px'
          }}>
            {results.found ? (
              <p>✅ Found {results.results.length} match(es) for "{results.query}"</p>
            ) : (
              <p>❌ No matches found for "{results.query}"</p>
            )}
          </div>

          {results.found && (
            <div style={{ marginTop: '15px' }}>
              {results.results.map((result, idx) => (
                <div key={idx} style={{
                  padding: '15px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  marginBottom: '10px',
                  background: 'white'
                }}>
                  <p><strong>Indicator:</strong> {result.indicator}</p>
                  <p><strong>Type:</strong> {result.type}</p>
                  <p><strong>Source:</strong> {result.source}</p>
                  <p><strong>Severity:</strong> 
                    <span style={{ 
                      color: result.severity === 'critical' ? '#dc3545' : 
                             result.severity === 'high' ? '#fd7e14' : 
                             result.severity === 'medium' ? '#ffc107' : '#28a745',
                      marginLeft: '5px',
                      fontWeight: 'bold'
                    }}>
                      {result.severity}
                    </span>
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchIoC;