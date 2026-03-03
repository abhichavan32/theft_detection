import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PredictionsList({ apiUrl }) {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchPredictions();
  }, [filter]);

  const fetchPredictions = async () => {
    setLoading(true);
    try {
      let url = `${apiUrl}/prediction-result/`;
      if (filter === 'theft') {
        url = `${apiUrl}/prediction-result/theft_only/`;
      }
      const response = await axios.get(url);
      setPredictions(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load predictions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading predictions...</div>;

  return (
    <div>
      <h2>All Predictions</h2>
      
      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ marginRight: '1rem' }}>Filter: </label>
        <button 
          className={filter === 'all' ? 'active' : ''} 
          onClick={() => setFilter('all')}
          style={{ marginRight: '0.5rem', padding: '0.5rem 1rem', cursor: 'pointer' }}
        >
          All
        </button>
        <button 
          className={filter === 'theft' ? 'active' : ''} 
          onClick={() => setFilter('theft')}
          style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
        >
          Theft Only
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {predictions.length === 0 ? (
        <p>No predictions found</p>
      ) : (
        <table className="predictions-table">
          <thead>
            <tr>
              <th>Meter ID</th>
              <th>Prediction</th>
              <th>Confidence</th>
              <th>LOF</th>
              <th>IF</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((pred, idx) => (
              <tr key={idx}>
                <td>{pred.meter_id}</td>
                <td>
                  <span className={`badge ${pred.voting_prediction}`}>
                    {pred.voting_prediction.toUpperCase()}
                  </span>
                </td>
                <td>{(pred.confidence * 100).toFixed(1)}%</td>
                <td>{pred.lof_prediction}</td>
                <td>{pred.if_prediction}</td>
                <td>{new Date(pred.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PredictionsList;
