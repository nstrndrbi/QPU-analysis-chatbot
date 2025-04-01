import React from 'react';
import './SuggestionChip.css';

const SuggestionChip = ({ text, onClick }) => {
  return (
    <div className="suggestion-chip" onClick={onClick}>
      {text}
    </div>
  );
};

export default SuggestionChip;
