import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Dashboard from './pages/Dashboard';
import PredictPage from './pages/PredictPage';
import PredictionsList from './pages/PredictionsList';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/electricity-data/stats/`);
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load statistics');
      console.error(err);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>⚡ Electricity Theft Detection System</h1>
        <nav className="nav">
          <button 
            className={currentPage === 'dashboard' ? 'active' : ''} 
            onClick={() => setCurrentPage('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={currentPage === 'predict' ? 'active' : ''} 
            onClick={() => setCurrentPage('predict')}
          >
            Predict
          </button>
          <button 
            className={currentPage === 'predictions' ? 'active' : ''} 
            onClick={() => setCurrentPage('predictions')}
          >
            Predictions
          </button>
        </nav>
      </header>

      <main className="main">
        {error && <div className="error">{error}</div>}
        
        {currentPage === 'dashboard' && <Dashboard stats={stats} />}
        {currentPage === 'predict' && <PredictPage apiUrl={API_URL} onPredict={fetchStats} />}
        {currentPage === 'predictions' && <PredictionsList apiUrl={API_URL} />}
      </main>

      <footer className="footer">
        <p>© 2026 Electricity Theft Detection | Powered by Django + React</p>
      </footer>
    </div>
  );
}

export default App;
