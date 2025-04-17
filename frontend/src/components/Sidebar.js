import React from 'react';

function Sidebar({ selectedTab, onSelectTab }) {
  const tabs = ["Charts", "Optimisation", "TeraOps Assistant"];

  return (
    <div className="Sidebar">
      {tabs.map((tab) => (
        <div
          key={tab}
          className={`Sidebar-tab ${selectedTab === tab ? 'active' : ''}`}
          onClick={() => onSelectTab(tab)}
        >
          {tab}
        </div>
      ))}
    </div>
  );
}

export default Sidebar;