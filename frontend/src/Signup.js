// src/Signup.js
// src/Signup.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const backendURL = process.env.REACT_APP_BACKEND_URL;

function Signup({ setAuth}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
 

  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      alert("❌ Please enter both username and password");
      return;
    }

    try {
      const res = await fetch(`${backendURL}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

        const text = await res.text();
        const data = text ? JSON.parse(text) : {};

      if (res.ok) {
        localStorage.setItem('jwt_token', data.access_token);
        localStorage.setItem('user', username);
        setAuth(true); // ✅ Save username
        alert("✅ Signup successful!");
        navigate('/dashboard');
      } else {
        alert(`❌ Signup failed: ${data.error || 'Unknown error'}`);
      }
    } catch (err) {
      alert(`❌ Signup error: ${err.message}`);
    }
  };

  return (
    <div className="auth-container">
      <h2>📝 Create a New Account</h2>
      <form onSubmit={handleSignup} className="auth-form">
        <input
          type="text"
          placeholder="👤 Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="🔒 Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button type="submit">✅ Create Account</button>
        <p className="auth-note">Already have an account? <a href="/login">Login</a></p>
      </form>
    </div>
  );
}

// Styles


export default Signup;
