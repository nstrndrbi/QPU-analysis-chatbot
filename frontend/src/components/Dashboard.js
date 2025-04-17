import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [summaryData, setSummaryData] = useState(null);
  const [efficiencyData, setEfficiencyData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSummaryData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/summary');
        const data = await response.json();
        setSummaryData(data);
      } catch (error) {
        console.error('Error fetching summary data:', error);
      }
    };

    const fetchEfficiencyData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/efficiency');
        const data = await response.json();
        setEfficiencyData(data);
      } catch (error) {
        console.error('Error fetching efficiency data:', error);
      }
    };

    Promise.all([fetchSummaryData(), fetchEfficiencyData()])
      .then(() => setIsLoading(false))
      .catch(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <div className="quantum-spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-core"></div>
        </div>
        <p>Loading QPU data...</p>
      </div>
    );
  }

  // Calculate average cost per workload from efficiency data
  const avgCostPerWorkload = efficiencyData.length 
    ? efficiencyData.reduce((sum, day) => sum + day.cost_per_workload, 0) / efficiencyData.length
    : 0;

  // Get the most recent atom block ratio
  const latestAtomRatio = efficiencyData.length 
    ? efficiencyData[efficiencyData.length - 1].atom_block_ratio
    : 0;

  return (
    <div className="dashboard">
      <h2 className="dashboard-title">
        <img src="/quantum-icon.png" alt="Quantum icon" className="dashboard-icon" />
        QPU Performance Summary
      </h2>

      <div className="dashboard-container">
        <div className="dashboard-card">
          <h3>
            <svg viewBox="0 0 24 24" className="icon">
              <path fill="currentColor" d="M11,7H15V9H11V11H13A2,2 0 0,1 15,13V15A2,2 0 0,1 13,17H9V15H13V13H11A2,2 0 0,1 9,11V9A2,2 0 0,1 11,7M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z" />
            </svg>
            QPU Blocks Leased
          </h3>
          <div className="stat-value">{summaryData?.total_blocks_leased || 0}</div>
          <div className="stat-detail">
            <div className="block-type atom">
              <span className="block-label">Atom</span>
              <span className="block-value">{summaryData?.atom_blocks || 0}</span>
            </div>
            <div className="block-type photon">
              <span className="block-label">Photon</span>
              <span className="block-value">{summaryData?.photon_blocks || 0}</span>
            </div>
            <div className="block-type spin">
              <span className="block-label">Spin</span>
              <span className="block-value">{summaryData?.spin_blocks || 0}</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card">
          <h3>
            <svg viewBox="0 0 24 24" className="icon">
              <path fill="currentColor" d="M21,5C19.89,4.65 18.67,4.5 17.5,4.5C15.55,4.5 13.45,4.9 12,6C10.55,4.9 8.45,4.5 6.5,4.5C4.55,4.5 2.45,4.9 1,6V20.65C1,20.9 1.25,21.15 1.5,21.15C1.6,21.15 1.65,21.1 1.75,21.1C3.1,20.45 5.05,20 6.5,20C8.45,20 10.55,20.4 12,21.5C13.35,20.65 15.8,20 17.5,20C19.15,20 20.85,20.3 22.25,21.05C22.35,21.1 22.4,21.1 22.5,21.1C22.75,21.1 23,20.85 23,20.6V6C22.4,5.55 21.75,5.25 21,5M21,18.5C19.9,18.15 18.7,18 17.5,18C15.8,18 13.35,18.65 12,19.5V8C13.35,7.15 15.8,6.5 17.5,6.5C18.7,6.5 19.9,6.65 21,7V18.5Z" />
            </svg>
            Total Workloads
          </h3>
          <div className="stat-value">{summaryData?.total_workloads?.toLocaleString() || 0}</div>
          <div className="stat-label">
            <span>Avg {summaryData?.avg_workloads_per_block || 0} workloads per block</span>
          </div>
          <div className="stat-label">
            <span>Avg {summaryData?.avg_daily_workloads?.toLocaleString() || 0} workloads per day</span>
          </div>
        </div>

        <div className="dashboard-card">
          <h3>
            <svg viewBox="0 0 24 24" className="icon">
              <path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,12.5A1.5,1.5 0 0,1 10.5,11A1.5,1.5 0 0,1 12,9.5A1.5,1.5 0 0,1 13.5,11A1.5,1.5 0 0,1 12,12.5M12,7.2C9.9,7.2 8.2,8.9 8.2,11C8.2,14 12,17.5 12,17.5C12,17.5 15.8,14 15.8,11C15.8,8.9 14.1,7.2 12,7.2Z" />
            </svg>
            Efficiency Metrics
            <span className="quantum-badge">Beta</span>
          </h3>
          <div className="stat-value">${avgCostPerWorkload.toFixed(2)}</div>
          <div className="stat-label">Average cost per workload</div>
          <div className="efficiency-meter">
            <div className="efficiency-label">Atom Block Ratio</div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${latestAtomRatio * 100}%` }}
              ></div>
            </div>
            <div className="efficiency-value">{(latestAtomRatio * 100).toFixed(1)}%</div>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <h4>Quick Analysis</h4>
        <div className="action-buttons">
          <a href="/api/graphs/costs" target="_blank" rel="noopener noreferrer">
            <button className="action-button">
              <svg viewBox="0 0 24 24" className="icon">
                <path fill="currentColor" d="M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z" />
              </svg>
              View Cost Trends
            </button>
          </a>
          <a href="/api/graphs/workloads" target="_blank" rel="noopener noreferrer">
            <button className="action-button">
              <svg viewBox="0 0 24 24" className="icon">
                <path fill="currentColor" d="M3,13H5V11H3V13M3,17H5V15H3V17M3,9H5V7H3V9M9,13H11V11H9V13M9,17H11V15H9V17M9,7H11V5H9V7M13,13H15V11H13V13M13,17H15V15H13V17M13,5H15V7H13V5M17,13H19V11H17V13M17,9H19V7H17V9M17,17H19V15H17V17Z" />
              </svg>
              Workload Analysis
            </button>
          </a>
          <a href="/api/graphs/efficiency" target="_blank" rel="noopener noreferrer">
            <button className="action-button">
              <svg viewBox="0 0 24 24" className="icon">
                <path fill="currentColor" d="M15,19L9,16.89V5L15,7.11M20.5,3C20.44,3 20.39,3 20.34,3L15,5.1L9,3L3.36,4.9C3.15,4.97 3,5.15 3,5.38V20.5A0.5,0.5 0 0,0 3.5,21C3.55,21 3.61,21 3.66,20.97L9,18.9L15,21L20.64,19.1C20.85,19 21,18.85 21,18.62V3.5A0.5,0.5 0 0,0 20.5,3Z" />
              </svg>
              Efficiency Metrics
            </button>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;