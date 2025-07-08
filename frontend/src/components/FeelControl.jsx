import React from 'react';

function FeelControl({ setFeelMode, feelRef, currentFeelMode }) {
  return (
    <div className="feel-control" ref={feelRef}>
      <h3>How do you want to feel?</h3>
      <div className="feel-buttons">
        <button
          className={`express-btn ${currentFeelMode === 'express' ? 'active' : ''}`}
          onClick={() => setFeelMode('express')}
        >
          Express
        </button>
        <button
          className={`calmdown-btn ${currentFeelMode === 'calmdown' ? 'active' : ''}`}
          onClick={() => setFeelMode('calmdown')}
        >
          Calm down
        </button>
      </div>
    </div>
  );
}

export default FeelControl;