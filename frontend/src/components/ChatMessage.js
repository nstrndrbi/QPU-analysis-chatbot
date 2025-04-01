import React from 'react';
import './ChatMessage.css';

const ChatMessage = ({ message }) => {
  const { text, sender, graph, isError } = message;
  
  const renderText = (text) => {
    // Handle text with line breaks
    return text.split('\n').map((line, i) => (
      <React.Fragment key={i}>
        {line}
        {i < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  return (
    <div className={`chat-message ${sender} ${isError ? 'error' : ''}`}>
      <div className="message-content">
        <div className="message-text">{renderText(text)}</div>
        {graph && (
          <div className="message-graph">
            <img src={`data:image/png;base64,${graph}`} alt="Cost trend graph" />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
