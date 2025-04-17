import React from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>QPU Analysis Chatbot</h1>

        <p>Ask questions about QPU blocks, costs, and trends</p>

      </header>
      <main>
        <ChatInterface />
      </main>
      <footer>
        <p>Powered by LangChain and Hugging Face</p>
      </footer>
    </div>
  );
}

export default App;
