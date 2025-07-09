// src/Toast.js
import React from 'react';
import './Toast.css';

function Toast({ type = 'info', message, onClose }) {
  return (
    <div className={`toast toast-${type}`}>
      <span>{message}</span>
      <button onClick={onClose} className="toast-close">&times;</button>
    </div>
  );
}

export default Toast;
