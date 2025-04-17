import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';
import ChatMessage from './ChatMessage';
import SuggestionChip from './SuggestionChip';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [activeTab, setActiveTab] = useState('chat');

  const suggestions = [
    'Tell me the top 10 most active QPU blocks',
    'What will happen to the cost if I only use Atom blocks?',
    'Generate a graph to show the trend of daily costs',
    'How can I optimize my block mix for better efficiency?',
    'Show me daily workload statistics'
  ];

  const tools = [
    { name: 'Cost Analysis', prompt: 'Analyze cost impact of different block types' },
    { name: 'Workload Graph', prompt: 'Generate a graph showing daily workloads' },
    { name: 'Efficiency Metrics', prompt: 'Show me block efficiency metrics over time' },
    { name: 'Block Mix Optimizer', prompt: 'How can I optimize my current block mix?' },
    { name: 'Scheduling Simulator', prompt: 'Simulate cost savings with batch scheduling' }
  ];

  // Add quantum particle effects for visual enhancement
  useEffect(() => {
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
      // Create quantum particles
      for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'quantum-particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        particle.style.animationDuration = `${15 + Math.random() * 15}s`;
        chatMessages.appendChild(particle);
      }
    }
    
    return () => {
      const particles = document.querySelectorAll('.quantum-particle');
      particles.forEach(particle => particle.remove());
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async (message = input) => {
    if (!message.trim()) return;

    const newUserMessage = {
      id: Date.now(),
      text: message,
      sender: 'user'
    };

    setMessages(prevMessages => [...prevMessages, newUserMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          history: messages.map(msg => ({
            user: msg.sender === 'user' ? msg.text : '',
            assistant: msg.sender === 'bot' ? msg.text : ''
          })).filter(item => item.user || item.assistant)
        }),
      });

      const data = await response.json();
      
      const newBotMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        graph: data.graph
      };

      setMessages(prevMessages => [...prevMessages, newBotMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error processing your request. Please try again.',
        sender: 'bot',
        isError: true
      };

      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToolSelect = (prompt) => {
    handleSend(prompt);
  };

  return (
    <div className="chat-interface">
      <div className="tabs-container">
        <div className="tab-buttons">
          <button 
            className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <svg viewBox="0 0 24 24" className="tab-icon">
              <path fill="currentColor" d="M12,3C17.5,3 22,6.58 22,11C22,15.42 17.5,19 12,19C10.76,19 9.57,18.82 8.47,18.5C5.55,21 2,21 2,21C4.33,18.67 4.7,17.1 4.75,16.5C3.05,15.07 2,13.13 2,11C2,6.58 6.5,3 12,3M17,12V10H15V12H17M13,12V10H11V12H13M9,12V10H7V12H9Z" />
            </svg>
            Chat
          </button>
          <button 
            className={`tab-button ${activeTab === 'tools' ? 'active' : ''}`}
            onClick={() => setActiveTab('tools')}
          >
            <svg viewBox="0 0 24 24" className="tab-icon">
              <path fill="currentColor" d="M21.71 20.29L20.29 21.71A1 1 0 0 1 18.88 21.71L7 9.85A3.81 3.81 0 0 1 6 10A4 4 0 0 1 2.22 4.7L4.76 7.24L5.29 6.71L6.71 5.29L7.24 4.76L4.7 2.22A4 4 0 0 1 10 6A3.81 3.81 0 0 1 9.85 7L21.71 18.88A1 1 0 0 1 21.71 20.29M2.29 18.88A1 1 0 0 0 2.29 20.29L3.71 21.71A1 1 0 0 0 5.12 21.71L10.59 16.25L7.76 13.42M20 2L16 4V6L13.83 8.17L15.83 10.17L18 8H20L22 4Z" />
            </svg>
            Tools
          </button>
        </div>
      </div>
      
      {activeTab === 'tools' && (
        <div className="tools-panel">
          <div className="tools-title">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10M10,22C9.75,22 9.54,21.82 9.5,21.58L9.13,18.93C8.5,18.68 7.96,18.34 7.44,17.94L4.95,18.95C4.73,19.03 4.46,18.95 4.34,18.73L2.34,15.27C2.21,15.05 2.27,14.78 2.46,14.63L4.57,12.97L4.5,12L4.57,11L2.46,9.37C2.27,9.22 2.21,8.95 2.34,8.73L4.34,5.27C4.46,5.05 4.73,4.96 4.95,5.05L7.44,6.05C7.96,5.66 8.5,5.32 9.13,5.07L9.5,2.42C9.54,2.18 9.75,2 10,2H14C14.25,2 14.46,2.18 14.5,2.42L14.87,5.07C15.5,5.32 16.04,5.66 16.56,6.05L19.05,5.05C19.27,4.96 19.54,5.05 19.66,5.27L21.66,8.73C21.79,8.95 21.73,9.22 21.54,9.37L19.43,11L19.5,12L19.43,13L21.54,14.63C21.73,14.78 21.79,15.05 21.66,15.27L19.66,18.73C19.54,18.95 19.27,19.04 19.05,18.95L16.56,17.95C16.04,18.34 15.5,18.68 14.87,18.93L14.5,21.58C14.46,21.82 14.25,22 14,22H10M11.25,4L10.88,6.61C9.68,6.86 8.62,7.5 7.85,8.39L5.44,7.35L4.69,8.65L6.8,10.2C6.4,11.37 6.4,12.64 6.8,13.8L4.68,15.36L5.43,16.66L7.86,15.62C8.63,16.5 9.68,17.14 10.87,17.38L11.24,20H12.76L13.13,17.39C14.32,17.14 15.37,16.5 16.14,15.62L18.57,16.66L19.32,15.36L17.2,13.81C17.6,12.64 17.6,11.37 17.2,10.2L19.31,8.65L18.56,7.35L16.15,8.39C15.38,7.5 14.32,6.86 13.12,6.62L12.75,4H11.25Z" />
            </svg>
            QPU Analysis Tools
          </div>
          <div className="tools-container">
            {tools.map((tool, index) => (
              <button 
                key={index} 
                className="tool-button"
                onClick={() => handleToolSelect(tool.prompt)}
              >
                {tool.name}
              </button>
            ))}
          </div>
        </div>
      )}
      
      <div className="chat-container">
        <div className="chat-header">
          <h3>
            <svg viewBox="0 0 24 24" width="24" height="24">
              <path fill="currentColor" d="M21,16.5C21,16.88 20.79,17.21 20.47,17.38L12.57,21.82C12.41,21.94 12.21,22 12,22C11.79,22 11.59,21.94 11.43,21.82L3.53,17.38C3.21,17.21 3,16.88 3,16.5V7.5C3,7.12 3.21,6.79 3.53,6.62L11.43,2.18C11.59,2.06 11.79,2 12,2C12.21,2 12.41,2.06 12.57,2.18L20.47,6.62C20.79,6.79 21,7.12 21,7.5V16.5M12,4.15L5,8.09V15.91L12,19.85L19,15.91V8.09L12,4.15M12,6.23L16.9,9.06L12,11.89L7.1,9.06L12,6.23M17,14.89L13,17.2V13.62L17,11.31V14.89M11,17.2L7,14.89V11.31L11,13.62V17.2Z" />
            </svg>
            QPU Agent
          </h3>
          <div className="chat-status">
            <span className="status-indicator"></span>
            Online
          </div>
        </div>
        
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h2>Hello! How can I help you with QPU analysis today?</h2>
              <div className="suggestions-container">
                {suggestions.map((suggestion, index) => (
                  <SuggestionChip 
                    key={index}
                    text={suggestion}
                    onClick={() => handleSend(suggestion)}
                  />
                ))}
              </div>
            </div>
          ) : (
            messages.map(message => (
              <ChatMessage 
                key={message.id}
                message={message}
              />
            ))
          )}
          {isLoading && (
            <div className="loading-indicator">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about QPU blocks, costs, or trends..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
          />
          <button 
            onClick={() => handleSend()} 
            disabled={!input.trim() || isLoading}
            className={!input.trim() || isLoading ? 'disabled' : ''}
          >
            <svg viewBox="0 0 24 24" width="18" height="18" style={{ marginRight: '6px' }}>
              <path fill="currentColor" d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
            </svg>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
