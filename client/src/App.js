import React from 'react';
import logo from './logo.svg';
import './App.css';
import PredictionComponent from './PredictionComponent';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1 style={{ textAlign: 'top', marginBottom: '120px' }}>Deception Detection</h1>
        <PredictionComponent />
      </header>
    </div>
  );
}

export default App;