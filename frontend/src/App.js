// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import Dashboard from './Dashboard';

// ✅ Route guard to check if JWT token exists
const isAuthenticated = () => {
  return !!localStorage.getItem("jwt_token");
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 🚪 Default route */}
        <Route path="/" element={<Navigate to={isAuthenticated() ? "/dashboard" : "/login"} />} />

        {/* 📝 Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* 🔒 Protected Dashboard */}
        <Route
          path="/dashboard"
          element={isAuthenticated() ? <Dashboard /> : <Navigate to="/login" />}
        />

        {/* 🚫 Fallback to Login if route not found */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
