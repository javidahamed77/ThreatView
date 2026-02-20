import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ThreatMap = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    setData([
      { country: 'USA', attacks: 45 },
      { country: 'Russia', attacks: 42 },
      { country: 'China', attacks: 38 },
      { country: 'Germany', attacks: 25 },
      { country: 'India', attacks: 30 },
    ]);
  }, []);

  return (
    <div style={{ marginTop: '30px' }}>
      <h3>Global Threat Map - Top Attack Sources</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="country" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="attacks" fill="#dc3545" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ThreatMap;