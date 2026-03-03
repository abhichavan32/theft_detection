import React, { useState } from 'react';
import axios from 'axios';

function PredictPage({ apiUrl, onPredict }) {
  const [formData, setFormData] = useState({
    daily_consumption: '',
    monthly_consumption: '',
    peak_hours_consumption: '',
    off_peak_hours_consumption: '',
    voltage_variation: '',
    current_variation: '',
    power_factor: '',
    reactive_power: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${apiUrl}/electricity-data/predict/`, formData);
      setResult(response.data);
      onPredict();
    } catch (err) {
      setError('Prediction failed: ' + (err.response?.data?.error || err.message));
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Make Prediction</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '0 auto', background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <div className="form-group">
          <label>Daily Consumption (kWh)</label>
          <input 
            type="number" 
            name="daily_consumption" 
            step="0.1"
            value={formData.daily_consumption}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Monthly Consumption (kWh)</label>
          <input 
            type="number" 
            name="monthly_consumption" 
            step="0.1"
            value={formData.monthly_consumption}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Peak Hours Consumption (kWh)</label>
          <input 
            type="number" 
            name="peak_hours_consumption" 
            step="0.1"
            value={formData.peak_hours_consumption}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Off-Peak Hours Consumption (kWh)</label>
          <input 
            type="number" 
            name="off_peak_hours_consumption" 
            step="0.1"
            value={formData.off_peak_hours_consumption}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Voltage Variation (±V)</label>
          <input 
            type="number" 
            name="voltage_variation" 
            step="0.1"
            value={formData.voltage_variation}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Current Variation (±A)</label>
          <input 
            type="number" 
            name="current_variation" 
            step="0.1"
            value={formData.current_variation}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Power Factor (0-1)</label>
          <input 
            type="number" 
            name="power_factor" 
            step="0.01"
            min="0"
            max="1"
            value={formData.power_factor}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Reactive Power (kVAR)</label>
          <input 
            type="number" 
            name="reactive_power" 
            step="0.1"
            value={formData.reactive_power}
            onChange={handleChange}
            required 
          />
        </div>

        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Processing...' : 'Predict'}
        </button>
      </form>

      {error && <div className="error" style={{ marginTop: '2rem' }}>{error}</div>}

      {result && (
        <div className={`result ${result.voting_prediction} theft`} style={{ marginTop: '2rem' }}>
          <h3>Prediction Result</h3>
          <p>
            <strong>Classification:</strong>
            <span className={`badge ${result.voting_prediction}`}>
              {result.voting_prediction.toUpperCase()}
            </span>
          </p>
          <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%</p>
          <p><strong>LOF Prediction:</strong> {result.lof_prediction} (Score: {result.lof_score.toFixed(4)})</p>
          <p><strong>IF Prediction:</strong> {result.if_prediction} (Score: {result.if_score.toFixed(4)})</p>
        </div>
      )}
    </div>
  );
}

export default PredictPage;
