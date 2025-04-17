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

    <div className="chat-container">
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
          Send
        </button>

      </div>
    </div>
  );
};

export default ChatInterface;
