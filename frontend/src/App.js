import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
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
    </div>
  );
}

export default App;
