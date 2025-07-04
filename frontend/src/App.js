import React from 'react';
import './App.css';

function App() {
  const handleDownload = (type) => {
    window.open(`http://localhost:5000/download/${type}`, '_blank');
  };

  return (
    <div className="App" style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1 style={{ marginBottom: "30px" }}>📊 AI Jira Summarizer Reports</h1>

      <button
        style={btnStyle}
        onClick={() => handleDownload('pdf')}
      >
        📄 Download PDF
      </button>

      <button
        style={btnStyle}
        onClick={() => handleDownload('csv')}
      >
        📊 Download CSV
      </button>

      <button
        style={btnStyle}
        onClick={() => handleDownload('json')}
      >
        🧾 Download JSON
      </button>
    </div>
  );
}

const btnStyle = {
  margin: '10px',
  padding: '12px 25px',
  background: '#4CAF50',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontSize: '16px'
};

export default App;
