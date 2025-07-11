// src/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const backendURL = process.env.REACT_APP_BACKEND_URL;

function Login({ setAuth }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`${backendURL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

        const text = await res.text();
        const data = text ? JSON.parse(text) : {};

      if (res.ok) {
        localStorage.setItem('jwt_token', data.access_token);
        localStorage.setItem('user', username); 
        setAuth(true);// ✅ Save username
        alert("✅ Login successful!");
        navigate('/dashboard');
      } else {
        alert(`❌ Login failed: ${data.error || 'Unknown error'}`);
      }
    } catch (err) {
      alert("❌ Login error: " + err.message);
    }
  };

  return (
    <div className="auth-container">
      <h2>🔐 Login to Continue</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        /><br /><br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br /><br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}


export default Login;
