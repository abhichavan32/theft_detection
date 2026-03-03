import React from 'react';

function Dashboard({ stats }) {
  if (!stats) {
    return <div className="dashboard"><p>Loading...</p></div>;
  }

  return (
    <div className="dashboard">
      <div className="stat-card">
        <h3>Total Records</h3>
        <div className="number">{stats.total_records || 0}</div>
      </div>
      <div className="stat-card">
        <h3>Theft Detected</h3>
        <div className="number" style={{ color: '#ff4444' }}>
          {stats.theft_detected || 0}
        </div>
      </div>
      <div className="stat-card">
        <h3>Normal Usage</h3>
        <div className="number" style={{ color: '#44aa44' }}>
          {stats.normal_detected || 0}
        </div>
      </div>
      <div className="stat-card">
        <h3>Accuracy</h3>
        <div className="number">
          {stats.accuracy ? (stats.accuracy * 100).toFixed(1) : 0}%
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
