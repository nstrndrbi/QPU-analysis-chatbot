import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
<<<<<<< HEAD
import Dashboard from './components/Dashboard';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard'); // 'dashboard' or 'chat'

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="logo-container">
            <img src="/quantum-logo.png" alt="QPU Analysis Logo" className="app-logo" />
            <h1>QPU Analysis Dashboard</h1>
          </div>
          <p className="header-description">
            Advanced analytics and intelligent insights for Quantum Processing Units
            <span className="quantum-badge">Agent-Powered</span>
          </p>
        </div>
        <div className="quantum-decoration">
          <div className="quantum-orbit"></div>
          <div className="quantum-orbit"></div>
          <div className="quantum-orbit"></div>
          <div className="quantum-core"></div>
        </div>
      </header>
      
      <nav className="main-nav">
        <button 
          className={`nav-button ${activeSection === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveSection('dashboard')}
        >
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z" />
          </svg>
          Dashboard
        </button>
        <button 
          className={`nav-button ${activeSection === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveSection('chat')}
        >
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M12,3C17.5,3 22,6.58 22,11C22,15.42 17.5,19 12,19C10.76,19 9.57,18.82 8.47,18.5C5.55,21 2,21C4.33,18.67 4.7,17.1 4.75,16.5C3.05,15.07 2,13.13 2,11C2,6.58 6.5,3 12,3M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z" />
          </svg>
          AI Assistant
        </button>
      </nav>
      
      <main>
        {activeSection === 'dashboard' ? <Dashboard /> : null}
        
        <div className={`chat-section ${activeSection === 'chat' ? 'active' : ''}`}>
          <ChatInterface />
        </div>
      </main>
      
      <footer>
        <div className="footer-content">
          <div className="footer-logo">
            <img src="/quantum-icon-small.png" alt="QPU" width="24" height="24" />
            <span>QPU Analysis Platform</span>
          </div>
          <div className="footer-links">
            <a href="#">Documentation</a>
            <a href="#">API</a>
            <a href="#">Support</a>
          </div>
          <div className="footer-info">
            <p>Powered by LangChain and Advanced LLM Technology</p>
            <p className="copyright">© 2025 QPU Analytics</p>
          </div>
        </div>
      </footer>
=======
import Sidebar from './components/Sidebar';

function App() {
  const [selectedTab, setSelectedTab] = useState("Chat interface");

  const renderContent = () => {
    switch (selectedTab) {
      case "Charts":
        return <div><h2>Charts</h2><p>Chart content goes here.</p></div>;
      case "Optimisation":
        return <div><h2>Optimisation Strategies</h2><p>Strategy content goes here.</p></div>;
      case "TeraOps Assistant":
      default:
        return <ChatInterface />;
    }
  };

  return (
    <div className="App">
      <Sidebar selectedTab={selectedTab} onSelectTab={setSelectedTab} />
      <div className="ContentArea">
        <header className="App-header">
          <h1>TeraOps Quantum Compute Optimisation Dashboard</h1>
          <p>Ask questions about QPU blocks, costs, trends and Optimisation Strategies</p>
        </header>
        <main>
          {renderContent()}
        </main>
      </div>
>>>>>>> caa328f1faa2d7ffc5310d4311684d2c6d4a18a7
    </div>
  );
}

export default App;
