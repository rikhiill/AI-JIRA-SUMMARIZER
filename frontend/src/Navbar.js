import React, { useState } from 'react';
import './Navbar.css';

function Navbar({ username = 'User', onLogout, theme, setTheme }) {
  const [showDropdown, setShowDropdown] = useState(false);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : theme === 'light' ? 'system' : 'dark';
    setTheme(newTheme);
  };

  return (
    <div className="navbar">
      <div className="brand">🚀 AI Jira Summarizer</div>
      <div className="navbar-user" onClick={() => setShowDropdown(!showDropdown)}>
        <div className="avatar">{username[0]?.toUpperCase()}</div>
        {showDropdown && (
          <div className="dropdown">
            <div className="dropdown-item">👤 {username}</div>
            <div className="dropdown-item" onClick={toggleTheme}>🌓 Theme: {theme}</div>
            <div className="dropdown-item" onClick={onLogout}>🚪 Logout</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Navbar;
